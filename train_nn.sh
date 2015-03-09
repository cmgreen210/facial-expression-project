#!/bin/bash

RUN_NAME=$1
MAX_IT=$2

PY='/usr/local/bin/python2.7'

BASE_DIR="/home/ec2-user/face-emotion-classifier"
CHK_DIR="${BASE_DIR}/checkpoint/${RUN_NAME}"
PARAMS="${CHK_DIR}/net_params.txt"
DATA="/home/ec2-user/data/fer_data.pkl"

OUTPUT="${CHK_DIR}/output.txt"

${PY} train_cnn.py \
    "${PARAMS}" "${CHK_DIR}/check_point" "${DATA}" "${MAX_IT}"\
> "${OUTPUT}"
