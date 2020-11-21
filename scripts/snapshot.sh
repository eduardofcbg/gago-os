#!/bin/bash

NOW=$(date +"%m-%d-%Y_%T")
cp -a /home/. /snapshots/${NOW}
