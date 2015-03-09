#!/bin/bash

NAME=$1

mkdir "checkpoint/${NAME}"

echo "learning_rate, 0.001, f
batch_size, 256,i
learning_rate_schedule, constant  ,
subtract_mean, False,b
random_mirror, True, b
momentum, 0.9, f" > "checkpoint/${NAME}/net_params.txt"