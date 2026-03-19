#!/usr/bin/env bash
.venv/bin/pelican content -o output -s publishconf.py

.venv/bin/ghp-import output -b gh-pages
git push git@github.com:ashleykleynhans/ashleykleynhans.github.io.git gh-pages:master --force
