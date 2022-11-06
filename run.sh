#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "No algorithm specified!"
    echo "Example: run.sh cluster input.csv"
    exit 1
fi

if [ -z "$2" ]; then
    echo "No input file given!"
    echo "Example: run.sh cluster input.csv"
    exit 1
fi

ALGO=$1
INPUT_FILE=$2
G_RADIUS="6000"
G_BF="180"

for i in 10 25 63 159 380; do
    echo "Computing for N = $i"
    COMMAND="\time -f \"Took %e seconds.\" python3.10 ./point_coverage.py -n $i -a $ALGO"

    if [ "$ALGO" == "clustering" ]; then
        eval "${COMMAND} -o output_${ALGO}_${i}.csv ${INPUT_FILE}"
        echo
    elif [ "$ALGO" == "graph" ]; then
        eval "${COMMAND} -r ${G_RADIUS} -b ${G_BF} -o output_${ALGO}_${i}.csv ${INPUT_FILE}"
        echo
    else
        echo "Aborted. Algorithm must be either 'clustering' or 'graph'!"
        exit 1
    fi
done
