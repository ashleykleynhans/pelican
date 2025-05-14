Title: Resolving macOS Kernel panic issues with Vagrant and Parallels
Date: 2025-05-14
Author: Ashley Kleynhans
Modified: 2025-05-14
Category: DevOps
Tags: macos, vagrant, parallels, vm
Summary: This post helps you to resolve macOS kernel panic issues
    when running Vagrant and Parallels with NFS synced folders.
Status: Published

## Introduction

I am running an Apple MacBook Pro with an Apple M1 Max chipset.
The Apple Silicon chipsets use `arm64` architecture, but when
I first started using Vagrant with the Parallels provider on
my M1 Max, Parallels didn't yet support shared/synced folders
on the `arm64` architecture, so I was using NFS for my
synced folders in my Vagrant development environment.

This worked perfectly until Apple released macOS Sequoia 15.4,
and then suddenly the synced folders across NFS constantly
caused macOS kernel panics resulting my laptop crashing.

## Debugging the issue

I was hopeful with every macOS Sequoia 15.4.x point release that
the issue would be resolved, but unfortunately the issue persisted
with every macOS Sequoia 15.4.x point release, and also in macOS
Sequoia 15.5.

When I inspected the crash files that were generated for sending
to Apple, it appeared as though there may have been issues with
my `NFS for Mac` application, so I uninstalled it, removed all
of its kernel extensions, and rebooted my laptop but unfortunately
the issue persisted.

I then finally realised that the issue was caused by using NFS
for my Parallels synced folders, and discovered that the latest
versions of Parallels now support shared folders on arm64
architecture.

## Resolving the issue

Changing all of my synced_folder configuration in my `Vagrantfile`
from `type: "nfs"` to `type: "parallels"` finally resolved the
issue, and I have not experienced a single macOS kernel panic
since.