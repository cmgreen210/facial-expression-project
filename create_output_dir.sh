#!/bin/bash

NAME=$1

mkdir "checkpoint/${NAME}"

echo "learning_rate, 0.001, f
batch_size, 100,i
learning_rate_schedule, constant  ,
subtract_mean, True,b
random_mirror, True, b
momentum, 0.9, f
l2_regularization, 0.0005, f
min_learning_rate, 0.00001, f
learning_rate_alpha, 0.5, f
learning_rate_gamma, 01, f
learning_rate_step, 1, i
init_random, gaussian,
init_sigma, 0.01,f
init_bias, 0.0,f
divideby, 255, f" > "checkpoint/${NAME}/net_params.txt"