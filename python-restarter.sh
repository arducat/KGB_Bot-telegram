#!/bin/bash

if [[ -z $1 ]]; then
  echo "Usage:"
  echo "$0 <path_to_python_file>"
  echo
  echo "Reruns the specified script if it fails."
  exit 1
fi

while true; do
  git pull >temp.log && python $1 2>>temp.log
  lastcode=$?

  if [[ $lastcode = 0 ]]; then
    echo "$1 completed without errors. Turning off..."
    exit
  elif [[ $lastcode = 2 ]]; then
    echo "Code 2, exit..."
    exit 2
  fi
  echo "$1 died (Error code $lastcode)"
done
