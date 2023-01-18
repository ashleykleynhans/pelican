Title: Upgrading Elastic Stack From 7.x to 8.x on Ubuntu 22.04
Date: 2023-01-18
Authors: Ashley Kleynhans
Modified: 2023-01-18
Category: DevOps
Tags: elastic, ubuntu, devops
Summary: In this post, I will walk you through the process that I followed to upgrade my Elastic Stack from version 7.x to 8.x on Ubuntu 22.04 LTS.

## Update apt repo from version 7.x to version 8.x

```bash
sudo mv /etc/apt/sources.list.d/elastic-7.x.list /etc/apt/sources.list.d/elastic-8.x.list
sudo vim /etc/apt/sources.list.d/elastic-8.x.list
```

Paste the following content:
```
deb [signed-by=/usr/share/keyrings/elastic.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main
```

## Upgrade packages

```bash
sudo apt update
sudo apt --only-upgrade install elasticsearch filebeat kibana logstash
```

## Update Elasticsearch config

```bash
sudo vim /etc/elasticsearch/elasticsearch.yml
```

Paste the following content, updating the cluster name as appropriate:
```
cluster.name: your-cluster-name
node.name: node-1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
discovery.type: single-node
xpack.security.enabled: false
xpack.security.enrollment.enabled: false

# Enable encryption for HTTP API client connections, such as Kibana, Logstash, and Agents
xpack.security.http.ssl:
  enabled: false

# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
  enabled: false

# Allow HTTP API connections from anywhere
# Connections are encrypted and require user authentication
http.host: 0.0.0.0
```

## Restart Elasticsearch

```bash
sudo systemctl restart elasticsearch
```

## Remove incompatible logging from Kibana systemd service

```bash
sudo vim /etc/systemd/system/kibana.service
```

Paste the following content:
```
[Unit]
Description=Kibana
Documentation=https://www.elastic.co
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=kibana
Group=kibana

Environment=KBN_HOME=/usr/share/kibana
Environment=KBN_PATH_CONF=/etc/kibana

EnvironmentFile=-/etc/default/kibana
EnvironmentFile=-/etc/sysconfig/kibana

ExecStart=/usr/share/kibana/bin/kibana --pid.file="/run/kibana/kibana.pid"

Restart=on-failure
RestartSec=3

StartLimitBurst=3
StartLimitInterval=60

WorkingDirectory=/usr/share/kibana

StandardOutput=journal
StandardError=inherit

[Install]
WantedBy=multi-user.target
```

## Restart Kibana

```bash
sudo systemctl restart kibana
```

## Verify all services are running

```bash
sudo systemctl status elasticsearch
sudo systemctl status logstash
sudo systemctl status kibana
```

## Verify version of Elasticsearch

```bash
curl http://127.0.0.1:9200
```
