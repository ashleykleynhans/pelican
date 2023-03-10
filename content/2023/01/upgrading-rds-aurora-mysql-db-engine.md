Title: Upgrading RDS Aurora MySQL DB Engine Version with Minimal Downtime
Date: 2023-01-19
Author: Ashley Kleynhans
Modified: 2023-03-02
Category: DevOps
Tags: devops, aws, rds, aurora, mysql
Summary: In this post, I will walk you through the process of upgrading an RDS Aurora MySQL DB engine with minimal downtime.
Status: Published

This procedure explains how to switch over from an existing
Aurora MySQL RDS cluster running a specific engine version to a
new Aurora MySQL RDS cluster running a new engine version
(eg. Upgrading the engine version of Aurora MySQL from 5.6 to
Aurora MySQL 5.7).  It has been tested successfully in upgrading
an Aurora MySQL from 5.6 to Aurora MySQL 5.7 and also upgrading
an Aurora MySQL from 5.7 to Aurora MySQL 8.

## Considerations before Upgrading from MySQL 5.7 to MySQL 8

If you are using ISO date formats when querying `DATETIME` fields,
your queries will no longer work in MySQL 8, so you will either need
to update your queries to use the correct `DATETIME` format, ie
`YYYY-MM-DD HH:MM:SS`, or to use the `STR_TO_DATE` function, eg:

```mysql
SELECT STR_TO_DATE( '2019-02-20T10:00:00.000Z', '%Y-%m-%dT%T.%fZ');
```

Otherwise you will run into errors that look like this:

```mysql
mysql> SELECT * FROM  example_table WHERE example_field >= '2023-01-02T06:45:31+0000';
ERROR 1525 (HY000): Incorrect DATETIME value: '2023-01-02T06:45:31+0000'
```

## Prepare for Upgrade

**It is important to create a new parameter group for each cluster
that you are upgrading so that you don't accidentally put another
production cluster into read only mode.**

* Add a DNS CNAME to point to the RDS load balancer for the current Aurora cluster
  with a TTL of **60 seconds**.
* Create a new DB Cluster parameter group with the same settings as the
  default parameter group.
* Change `binlog_format` from either `OFF` (this was the default in 5.6)
  or `ROW` (this was the default in 5.7) to `MIXED` in the new
  Parameter group.
* Add a new Reader instance to the cluster.
* Modify the new Reader instance to use the new DB Cluster Parameter Group.
* Apply the changes immediately.
* Reboot the new Reader instance for the Parameter Group changes to
  take effect.
* Failover the new Reader instance so that it becomes the Master/Writer so that
  the cluster does not need to be rebooted for the parameter group changes to take effect.
* Confirm that `binlog_format` is enabled on the new Writer instance that you
  failed over to in point (4) above.
```bash
SHOW VARIABLES LIKE 'binlog_format';
```
The output should look like this:
```bash
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | MIXED |
+---------------+-------+
1 row in set (0.00 sec)
```
* Confirm that the new Writer is able to replicate to a new cluster:
```bash
SHOW MASTER STATUS;
```
**If nothing is returned, replication is not enabled and you need to investigate
before proceeding.**

* Check binlog rotation time, increase to 24 hours minimum:
```bash
CALL mysql.rds_show_configuration();
CALL mysql.rds_set_configuration('binlog retention hours', 24);
```
* Create a user to set up replication:
```bash
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* to '<USERNAME>'@'%' IDENTIFIED BY '<PASSWORD>';
```

## Start the Upgrade
### Restore Snapshot to the new Aurora DB Engine Version

* Check binlog positions:
```bash
SHOW MASTER STATUS;
```
* Take a snapshot of the read replica.
* Restore the snapshot into a new Aurora cluster using the new DB engine version.
* Configure the Writer in the new Aurora cluster to replicate from the Aurora
   cluster running the old engine version:
```bash
CALL mysql.rds_set_external_master('<MASTER_ENDPOINT>', 3306, '<USERNAME>', '<PASSWORD>','<BINLOG_FILE>', '<BINLOG_POSITION>', 0);
CALL mysql.rds_start_replication;
```
* Check that there is no replication lag, and wait for the slave to catch up
   to master (ensure that `Seconds_Behind_Master` is `0`):
```bash
SHOW SLAVE STATUS\G
```
* Create a read replica in the new Aurora cluster running the new DB engine version.

### Swing over to new Aurora Cluster

* Put application into maintenance mode.
* Edit parameter group and change `read_only` from `{TrueIfReplica}` to 1 to prevent writes
   to the old cluster (no reboot required).
* Update DNS CNAME to point to the new RDS Cluster endpoint.
* Reset the new master/writer in the new Aurora cluster:
```bash
CALL mysql.rds_reset_external_master;
```
* Take application out of maintenance mode.
* Stop the old Aurora Cluster.
* Test.
* Start and delete the old Cluster after a few days (it cannot be deleted
   when it is stopped).

## Rolling back

* Start the old Aurora Cluster.
* Once the old cluster is up, put application into maintenance mode.
* Update DNS CNAME to point back to the old RDS Cluster endpoint.
* Edit parameter group and change `read_only` back from `1` to
  `{TrueIfReplica}` to enable writes the cluster (no reboot required).
* Take application out of maintenance mode.
* Test.

## References

* [Upgrading to RDS MySQL 8.0 with minimum downtime](
   https://blogs.halodoc.io/upgrading-to-rds-mysql-8-0-with-minimum-downtime/)
* [How do I turn on binary logging for my Amazon Aurora MySQL cluster?](
   https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/)