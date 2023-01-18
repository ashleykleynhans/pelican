#!/usr/bin/env bash
pelican content -o output -s pelicanconf.py
ghp-import output -b gh-pages
git push git@github.com:ashleykleynhans/ashleykleynhans.github.io.git gh-pages:master --force
