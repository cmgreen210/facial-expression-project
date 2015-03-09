#!/bin/bash

NAME=$1

mkdir "checkpoint/${NAME}"

echo "learning_rate, 0.001, f
batch_size, 128,i
learning_rate_schedule, constant  ,
subtract_mean, False,b
random_mirror, True, b" > "checkpoint/${NAME}/net_params.txt"