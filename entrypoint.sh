#!/bin/bash

set -e
echo root:${PASS} | chpasswd
/usr/sbin/sshd -D
