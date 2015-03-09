#!/bin/bash

RUN_NAME=$1
BASE_DIR="/home/ec2-user/face-emotion-classifier"
CHK_DIR="${BASE_DIR}/checkpoint/${RUN_NAME}"

crontab -l > mycron
echo "*/5 * * * * /usr/lib/sendmail cmgreen210@gmail.com" < \
        "${CHK_DIR}/output.txt"
crontab mycron
rm mycron
