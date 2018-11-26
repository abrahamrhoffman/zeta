#!/bin/bash

function startCluster () {
  cd /var/log
  nohup dask-scheduler --port 8445 &> scheduler.log&
  nohup dask-worker tcp://localhost:8445 &> worker.log&
}

function startAPI () {
  cd /x/src
  python /x/src/api/api.py
}

function main () {
  startCluster
  startAPI
  sleep infinity
}

main
