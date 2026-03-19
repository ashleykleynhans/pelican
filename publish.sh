#!/usr/bin/env bash
/Users/ashley/src/personal/blog/.venv/bin/pelican content -o output -s publishconf.py

# This can remove your new articles so add them in first
cp index.html output/index.html

ghp-import output -b gh-pages
git push git@github.com:ashleykleynhans/ashleykleynhans.github.io.git gh-pages:master --force
