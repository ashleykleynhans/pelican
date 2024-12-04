#!/usr/bin/env bash
pelican content -o output -s publishconf.py

# This can remove your new articles so add them in first
cp index.html output/index.html

ghp-import output -b gh-pages
git push git@github.com:ashleykleynhans/ashleykleynhans.github.io.git gh-pages:master --force
