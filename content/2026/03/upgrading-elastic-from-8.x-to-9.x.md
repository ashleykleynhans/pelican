Title: Upgrading Elastic Stack From 8.x to 9.x on Ubuntu 24.04
Date: 2026-03-26
Author: Ashley Kleynhans
Modified: 2026-03-26
Category: DevOps
Tags: elastic, ubuntu, devops
Summary: In this post, I will walk you through the process that I followed to upgrade my Elastic Stack from version 8.x to 9.x on Ubuntu 24.04 LTS.
Status: Published

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
sudo systemctl start filebeat
```

## Step 7: Verify

```bash
curl -s localhost:9200 | grep number
curl -s localhost:9200/_cluster/health?pretty
```
