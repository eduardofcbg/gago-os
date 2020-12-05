#!/bin/bash

NOW=$(date +"%d-%m-%Y_%T")
cp -a /home/. /snapshots/${NOW}
