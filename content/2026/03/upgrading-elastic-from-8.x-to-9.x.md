Title: Upgrading Elastic Stack From 8.x to 9.x on Ubuntu 24.04
Date: 2026-03-26
Author: Ashley Kleynhans
Modified: 2026-04-13
Category: DevOps
Tags: elastic, ubuntu, devops
Summary: In this post, I will walk you through the process that I followed to upgrade my Elastic Stack from version 8.x to 9.x on Ubuntu 24.04 LTS.
Status: Published

## Prerequisites

Before upgrading to 9.x, you need to be running **8.19.x**. See the
[official upgrade path](https://www.elastic.co/docs/deploy-manage/upgrade/deployment-or-cluster/upgrade-717){:target="_blank"}
for details.

Check your current version:

```bash
curl -s localhost:9200 | grep number
```

If you are not on 8.19.x, upgrade within the 8.x repo first before
switching to 9.x.

## Step 1: Fix GPG Key

The 9.x packages use an updated GPG key. Re-import it in the dearmored
keyring format:

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | \
  sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

## Step 2: Switch Repo to 9.x

```bash
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] \
https://artifacts.elastic.co/packages/9.x/apt stable main" | \
sudo tee /etc/apt/sources.list.d/elastic.list

sudo apt update
```

## Step 3: Upgrade Elasticsearch

```bash
sudo systemctl stop elasticsearch
sudo apt install --only-upgrade elasticsearch
sudo systemctl daemon-reload
sudo systemctl start elasticsearch
curl -s localhost:9200 | grep number
```

## Step 4: Upgrade Kibana

```bash
sudo systemctl stop kibana
sudo apt install --only-upgrade kibana
```

### Fix Missing Encryption Key

!!! danger
    Kibana 9.x requires encryption keys to be set. Without them Kibana
    will return **500 errors** on startup.

Generate the keys:

```bash
sudo /usr/share/kibana/bin/kibana-encryption-keys generate
```

Add the three generated lines to the bottom of `/etc/kibana/kibana.yml`:

```yaml
xpack.encryptedSavedObjects.encryptionKey: "your-generated-key-here"
xpack.reporting.encryptionKey: "your-generated-key-here"
xpack.security.encryptionKey: "your-generated-key-here"
```

Then start Kibana:

```bash
sudo systemctl daemon-reload
sudo systemctl start kibana
```

## Step 5: Upgrade Logstash

```bash
sudo systemctl stop logstash
sudo apt install --only-upgrade logstash
sudo systemctl daemon-reload
sudo systemctl start logstash
```

## Step 6: Upgrade Other Components (if installed)

### Filebeat

```bash
sudo systemctl stop filebeat
sudo apt install --only-upgrade filebeat
sudo systemctl daemon-reload
sudo systemctl start filebeat
```

#### Unique `id` Required for Every `filestream` Input

From Filebeat 9.x onwards, **every `filestream` input must have a
unique `id`**. If two or more `filestream` inputs share the same
`id` (or any of them omits `id` entirely), Filebeat will refuse to
start and log an error similar to:

```
filestream input with ID 'my-id' already exists, this will
lead to data duplication, please use a different ID
```

Review `/etc/filebeat/filebeat.yml` and every file under
`/etc/filebeat/inputs.d/` (or whichever
`filebeat.config.inputs.path` points at) and make sure each
`- type: filestream` block has its own distinct `id`:

```yaml
filebeat.inputs:
  - type: filestream
    id: nginx-access
    paths:
      - /var/log/nginx/access.log

  - type: filestream
    id: nginx-error
    paths:
      - /var/log/nginx/error.log
```

After fixing the IDs, restart Filebeat and confirm it is running:

```bash
sudo systemctl restart filebeat
sudo systemctl status filebeat
```

## Step 7: Verify

```bash
curl -s localhost:9200 | grep number
curl -s localhost:9200/_cluster/health?pretty
```

## References

- [Elasticsearch Release Notes](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-release-notes.html){:target="_blank"}
- [Upgrade your deployment or cluster](https://www.elastic.co/docs/deploy-manage/upgrade/deployment-or-cluster){:target="_blank"}
- [Upgrading Logstash](https://www.elastic.co/guide/en/logstash/current/upgrading-logstash.html){:target="_blank"}
- [Upgrading Filebeat](https://www.elastic.co/guide/en/beats/libbeat/current/upgrading.html){:target="_blank"}
- [Kibana Encryption Keys](https://www.elastic.co/guide/en/kibana/current/kibana-encryption-keys.html){:target="_blank"}
- [Elastic APT Repository](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html){:target="_blank"}
