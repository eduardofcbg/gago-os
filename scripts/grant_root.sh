#!/bin/bash

cat /config/$1 | while read user 
do
   usermod -aG sudo $user
done
