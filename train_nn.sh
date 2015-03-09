#!/bin/bash

RUN_NAME = $1
MAX_IT = $2

BASE_DIR = "/home/ec2-user/face-emotion-classifier"
CHK_DIR = "${BASE_DIR}/checkpoint/${RUN_NAME}"
PARAMS = "${CHK_DIR}/net_params.txt"
DATA = "/home/ec2-user/data/fer_data.pkl"

OUTPUT = "${CHK_DIR}/output.txt"

/usr/local/bin/python train_cnn.py "${PARAMS}" "${CHK_DIR}" "${DATA}" > "${OUTPUT}"


