#!/bin/bash

cat ../config/users.txt | while read user 
do
   useradd -s /bin/bash -m $user
   echo "$user:$user" | chpasswd
   passwd --expire $user
done
