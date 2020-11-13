#!/bin/bash

cat ../users.txt | while read user 
do
   useradd -m $user
   echo "$user:$user" | chpasswd
   passwd --expire $user
done
