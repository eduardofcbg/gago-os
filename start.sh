#!/bin/bash

docker-compose rm -fs
docker-compose up --build "$@"
