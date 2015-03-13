#!/bin/bash

# MODEL is the path to the neural net config
# MAX_IT is the maximum number of iterations
# DATA Path to pickled fer files
MODEL=$1
MAX_IT=$2
DATA=$3

PY='/usr/local/bin/python2.7'

if [ ! -d "checkpoint" ]; then
    mkdir "checkpoint"
fi

STAMP=$(date +"%Y%m%d_%H%M%S")
OUT_DIR="checkpoint/train_$STAMP"

if [ -d "${OUT_DIR}" ]; then
    rm -rf "${OUT_DIR}"
fi

mkdir "${OUT_DIR}"

PARAMS="${OUT_DIR}/net.conf"
cp "${MODEL}" "${OUT_DIR}/net.conf"

OUTPUT="${OUT_DIR}/output.txt"

${PY} train_nn.py \
    "${PARAMS}" "${OUT_DIR}" "${DATA}" "${MAX_IT}"\
> "${OUTPUT}"
