#!/usr/bin/env bash
set -e

# Rebuild minified theme assets (style.min.css, dark-theme.min.js) from source
# so the published site never serves stale minified files.
make assets

.venv/bin/pelican content -o output -s publishconf.py

.venv/bin/ghp-import output -b gh-pages
git push git@github.com:ashleykleynhans/ashleykleynhans.github.io.git gh-pages:master --force
