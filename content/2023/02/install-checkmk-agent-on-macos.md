Title: Installing CheckMK Agent on macOS
Date: 2023-02-03
Author: Ashley Kleynhans
Modified: 2023-02-03
Category: DevOps
Tags: devops, checkmk, monitoring, macos
Summary: This post walks you through the process of installing CheckMK
    agent on macOS servers so that they can be monitored by your
    CheckMK server.
Status: Published

## Installation Procedure

You can install CheckMK agent on your macOS servers as follows:

```bash
# Clone Repo
git clone https://github.com/ThomasKaiser/Check_MK.git
cd Check_MK

# Remove less common plugins
rm -f agents/plugins/monitor-jss-and-macos-updates agents/plugins/city-temperatures agents/plugins/monitor-kerio agents/plugins/smart*

# Install dependencies
brew install smartmontools osx-cpu-temp

# Modify the plist file (remove cwd)
sed -i '' '/<key>WorkingDirectory/{N;d;}' LaunchDaemon/de.mathias-kettner.check_mk.plist

# Create directories needed and copy files to required location
sudo mkdir -p /usr/local/lib/check_mk_agent
sudo mkdir /usr/local/lib/check_mk_agent/local
sudo cp agents/check_mk_agent.macosx /usr/local/lib/check_mk_agent/
sudo cp -r agents/plugins/ /usr/local/lib/check_mk_agent/
sudo cp LaunchDaemon/de.mathias-kettner.check_mk.plist /Library/LaunchDaemons/
sudo mkdir -p /usr/local/bin
sudo ln -s /usr/local/lib/check_mk_agent/check_mk_agent.macosx /usr/local/bin/check_mk_agent
sudo mkdir /etc/check_mk

sudo touch /var/run/de.arts-others.softwareupdatecheck
sudo touch /var/log/check_mk.err

# Permissions
sudo chmod +x /usr/local/lib/check_mk_agent/check_mk_agent.macosx
sudo chmod o+rw /var/run/de.arts-others.softwareupdatecheck
sudo chmod 666 /var/log/check_mk.err
sudo chown -R root:admin /usr/local/lib/check_mk_agent
sudo chmod 644 /Library/LaunchDaemons/de.mathias-kettner.check_mk.plist

# Install LaunchDaemon
sudo launchctl load -w /Library/LaunchDaemons/de.mathias-kettner.check_mk.plist

# Once lnx_if fix is merged into the agent, the below is required (see: https://github.com/ThomasKaiser/Check_MK/pull/2)
brew install iproute2mac
```

## Reference

* [Install check_mk agent on OSX](https://gist.github.com/catchdave/44c45e31951fcc9ee4fb8768f4d95f21)