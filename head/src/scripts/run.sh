#!/bin/bash

function startHead () {
  ray start --head \
            --redis-port=6379 \
            --num-redis-shards=2 \
            --redis-shard-ports=6380,6381  \
            --object-manager-port=2384
}

function startAPI () {
  cd /x/src
  python /x/src/api/api.py
}

function main () {
  startHead
  startAPI
  sleep infinity
}

main
