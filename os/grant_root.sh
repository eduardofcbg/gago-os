#!/bin/bash

cat ../users.txt | while read user 
do
   usermod -aG sudo $user
done
