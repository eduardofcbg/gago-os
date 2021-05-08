#!/bin/bash

now=$(date +"%Y-%m-%d_%H_%M_%S")
destination=/snapshots/${now}.zip

cd home
zip -r $destination .

echo "Snapshot saved at $destination"
