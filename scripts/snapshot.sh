#!/bin/bash

now=$(date +"%d-%m-%Y_%T")
destination=/snapshots/${now}

cp -a /home/. $destination

echo Snapshot saved at $destination
