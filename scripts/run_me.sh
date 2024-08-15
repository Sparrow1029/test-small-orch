#!/bin/bash
echo "Running the calculation..."
loop=0
while [[ $loop -lt 5 ]]; do
  echo "Iteration: ${loop}"
  sleep 2
  let loop++
done
echo "Done!"
