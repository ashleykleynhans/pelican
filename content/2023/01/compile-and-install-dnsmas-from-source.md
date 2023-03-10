Title: Compiling and Installing dnsmasq from Source on Ubuntu 22.04
Date: 2023-01-19
Author: Ashley Kleynhans
Modified: 2023-01-19
Category: DevOps
Tags: devops, dns, dnsmasq, nginx
Summary: This post walks you through the process of compiling and
    installing dnsmasq 2.88 from source in Ubuntu 22.04, so that you
    can benefit from the `filter-AAAA` feature that was introduced
    in dnsmasq version 2.87 in order to resolve issues with nginx
    servers that only have IPv4 addresses attached to them getting
    network unreachable errors when resolving upstream DNS entries
    to IPv6 addresses.
Status: Published

## Background

I was monitoring my nginx logs, when I stumbled across a
peculiar error where nginx was trying to connect to a
Firebase backend with a DNS entry that resolves to an
IPv6 address.

<pre>
[nginx][] 2023/01/06 07:32:38 [error] 61125#61125: *4683 connect() to
[fe80::cf4d:cab8:b943]:443 failed (101: Network is unreachable) while
connecting to upstream, client: 1.1.1.1, server: , request: 
"GET /file.json?v=3 HTTP/2.0", upstream: 
"https://[fe80::cf4d:cab8:b943]:443/file.json?v=3", host: "example.com", 
referrer: "https://example.com/worker.js"
</pre>

This was rather perplexing, since none of my nginx servers
have any IPv6 addresses attached to them, but discovered that
the DNS lookup for my Firebase application was returning the
same IPv6 address that I noticed in my nginx log file.

```bash
$ host example-app.firebaseapp.com
example-app.firebaseapp.com has address 192.168.1.1
example-app.firebaseapp.com has IPv6 address fe80::cf4d:cab8:b943
```

I then determined that the best way to solve this problem would
be to set up dnsmasq as a DNS cache, and use the `filter-AAAA`
option to prevent it from performing IPv6 lookups.

The problem with this, however, is that the latest version of
the dnsmasq package in the Ubuntu 22.04 repositories is
version **2.86** and the `filter-AAAA` feature was only
introduced in dnsmasq version **2.87**.

[Ubuntu 23.04 (Lunar Lobster)](https://launchpad.net/ubuntu/lunar/+source/dnsmasq),
which is currently under active  development at the time of writing,
is the only Ubuntu version that has a version of dnsmasq that
supports the `filter-AAAA` feature, so I decided to compile
and install dnsmasq from the [source used by Ubuntu 23.04](
https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/dnsmasq/2.88-1/dnsmasq_2.88.orig.tar.gz).

## Download, Compile and Install dnsmasq from Source

### Download source for dnsmasq version 2.88 from Ubuntu Launchpad site

```bash
cd /tmp
wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/dnsmasq/2.88-1/dnsmasq_2.88.orig.tar.gz
```

### Extract dnsmasq 2.88 source

```bash
tar zxvf dnsmasq_2.88.orig.tar.gz
```

### Install dependency packages

```bash
sudo apt update
sudo apt install dnsmasq gettext
```

### Compile dnsmasq

```bash
cd dnsmasq-2.88.orig
make all-i18n
```

### Confirm the version of the compiled dnsmasq binary

```bash
src/dnsmasq -v
```

### Stop the dnsmasq service

```bash
sudo systemctl stop dnsmasq
```

### Copy the newly compiled binary over the old one

```bash
sudo cp src/dnsmasq /usr/sbin/dnsmasq
```

### Remove file that is no longer supported by the new binary

```bash
sudo rm /usr/share/dns/root.ds
```

### Edit the dnsmasq config file and configure it to exclude IPv6 lookups

```bash
sudo vim /etc/dnsmasq.conf
```

Paste the following content:
```
listen-address=127.0.0.53
port=53
bind-interfaces
user=dnsmasq
group=nogroup
pid-file=/var/run/dnsmasq/dnsmasq.pid

# Name resolution options
resolv-file=/etc/resolv.dnsmasq
cache-size=500
neg-ttl=60
domain-needed
bogus-priv
filter-AAAA
```
And save the file.

### Configure the DNS resolver for the dnsmasq service

```bash
sudo bash -c "echo 'nameserver 1.1.1.1' > /etc/resolv.dnsmasq"
```

### Configure DNS resolver for Consul (OPTIONAL)

```bash
sudo vim /etc/dnsmasq.d/10-consul
```

Paste the following content:
```
server=/consul/127.0.0.1#8600
```
And save the file.

### Disable systemd resolved

```bash
sudo vim /etc/systemd/resolved.conf.d/noresolved.conf
```

Paste the following content:
```
[Resolve]
DNSStubListener=no
```
And save the file.

### Restart the systemd-resolved and dnsmasq services

```bash
sudo systemctl restart systemd-resolved
sudo systemctl restart dnsmasq.service
```

### Edit /etc/resolv.conf to use dnsmasq as the DNS resolver

```bash
sudo vim /etc/resolv.conf
```

Paste the following content:
```
nameserver 127.0.0.53
```
And save the file.

## Verify that the DNS is now only resolving to IPv4 addresses and not IPv6 anymore

```bash
$ host example-app.firebaseapp.com
example-app.firebaseapp.com has address 192.168.1.1
```