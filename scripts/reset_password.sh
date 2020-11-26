#!/bin/bash

user=$1
echo "$user:$user" | chpasswd
passwd --expire $user
