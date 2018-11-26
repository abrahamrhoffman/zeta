#!/bin/bash

function startAPI () {
  cd /zeta-ui/api
  nohup python zeta-api.py &> /zeta-api.log&
}

function startUI () {
  cd /zeta-ui
  nohup yarn start &> /zeta-ui.log&
}

function main () {
  startUI
  sleep infinity
}

main
