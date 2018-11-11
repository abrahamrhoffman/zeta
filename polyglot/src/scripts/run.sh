#!/bin/bash

function startAPI () {
  cd /x/src
  python /x/src/api/api.py
}

function main () {
  startAPI
  sleep infinity
}

main
