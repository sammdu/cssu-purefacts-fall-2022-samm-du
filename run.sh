#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "No input file given!"
    echo "Example: run.sh input.csv"
    exit 1
fi

INPUT_FILE=$1
for i in 10 25 63 159 380; do
    echo "Computing for N = $i"
    python3.10 ./point_coverage.py -n "$i" -o "output_$i.csv" "$INPUT_FILE"
done
