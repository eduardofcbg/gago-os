#!/bin/bash

cat ../config/users.txt | while read user 
do
   usermod -aG sudo $user
done
