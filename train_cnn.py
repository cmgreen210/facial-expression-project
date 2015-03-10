from __future__ import print_function
from fec.classifier.gl_nn import GraphLabNeuralNetBuilder
from fec.classifier.gl_classifier import GraphLabClassifierFromNetBuilder
import pandas as pd
import numpy as np
import sys
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score, f1_score
from os.path import join as pjoin
import os.path as opath

def simple_net_1(net):
    #   ----Conv
    stride = 1
    num_channels = 32
    kernel_size = 5

    kwargs = {'padding': 2}
    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)

    # ---Max Pooling---
    padding = 0
    stride = 2
    kernel_size = 3

    net.add_max_pooling_layer(kernel_size, stride, padding)

    # ---Flatten---
    net.add_flatten_layer()

    #-----Fully Connected-----
    num_hidden_units = 256

    net.add_full_connection_layer(num_hidden_units)

    #----ReLu-------
    net.add_relu_layer()

    #----Drop Out----
    threshold = 0.3
    net.add_dropout_layer(threshold=threshold)

    #-----Fully Connected-----
    num_hidden_units = 3

    net.add_full_connection_layer(num_hidden_units)

    #---SOFTMAX----
    net.add_soft_max_layer()
    return net


def create_net_kag(net):
    #-------1st Convolution Layer---------
    stride = 1
    num_channels = 32
    kernel_size = 5

    kwargs = {'padding': 2}

    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)
    net.add_relu_layer()

    # Pooling Layer
    padding = 0
    stride = 2
    kernel_size = 3

    net.add_max_pooling_layer(kernel_size, stride, padding)

    #-------2nd Convolution Layer---------
    stride =2
    num_channels = 32
    kernel_size = 4

    kwargs = {'padding': 1}

    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)
    net.add_relu_layer()

    # Pooling Layer
    padding = 0
    stride = 2
    kernel_size = 3

    net.add_max_pooling_layer(kernel_size, stride, padding)

    #-------3rd Convolution Layer---------
    stride = 1
    num_channels = 64
    kernel_size = 5

    kwargs = {'padding': 2}

    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)
    net.add_relu_layer()

    # Pooling Layer
    padding = 0
    stride = 2
    kernel_size = 3

    net.add_max_pooling_layer(kernel_size, stride, padding)

    # Flatten Layer
    net.add_flatten_layer()

    # Fully Connected Layer 1
    num_hidden_units = 3072

    net.add_full_connection_layer(num_hidden_units)

    # Fully Connected Layer
    num_hidden_units = 7  # Number of class labels

    net.add_full_connection_layer(num_hidden_units)

    # Soft Max Layer
    net.add_soft_max_layer()

    return net


def create_net_2_conv(net):
    #   ----Conv
    stride = 1
    num_channels = 32
    kernel_size = 3

    kwargs = {'padding': 1}
    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)

    # RELU
    net.add_relu_layer()

    # ---Max Pooling---
    padding = 0
    stride = 2
    kernel_size = 2

    net.add_max_pooling_layer(kernel_size, stride, padding)

    #   ----Conv
    stride = 1
    num_channels = 64
    kernel_size = 3

    kwargs = {'padding': 1}
    net.add_convolution_layer(kernel_size, stride, num_channels, **kwargs)

    # RELU
    net.add_relu_layer()

    # ---Max Pooling---
    padding = 0
    stride = 2
    kernel_size = 2

    net.add_max_pooling_layer(kernel_size, stride, padding)

    #-----Fully Connected-----
    net.add_flatten_layer()

    num_hidden_units = 256

    net.add_full_connection_layer(num_hidden_units)

    #-----Fully Connected-----
    num_hidden_units = 7

    net.add_full_connection_layer(num_hidden_units)

    #---SOFTMAX----
    net.add_soft_max_layer()
    return net

if __name__ == '__main__':
    # Create network builder and set network parameters
    net = GraphLabNeuralNetBuilder()

    net.set_params_from_file(sys.argv[1])
    check_point_path = sys.argv[2]
    data_path = sys.argv[3]
    max_iterations = int(sys.argv[4])
    if sys.argv[5] == '':
        exit()
    model = int(sys.argv[5])

    if model == 1:
        net = simple_net_1(net)
    else:
        exit()

    df = pd.read_pickle(data_path)

    cond_happy = df['emotion'] == 3
    cond_sad = df['emotion'] == 2
    cond_surprise = df['emotion'] == 5

    df = df[cond_happy | cond_sad | cond_surprise]

    x = np.array(df['pixels'].tolist())
    y = np.array(df['emotion'].values)

    xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=.8)

    model = GraphLabClassifierFromNetBuilder(net, chkpt_dir=check_point_path,
                                             max_iterations=max_iterations,
                                             train_frac=.8)
    model.fit(xtrain, ytrain)

    eval = model.evaluate(xtest, ytest, metric=['accuracy', 'confusion_matrix',
                                               'recall@1', 'recall@2'])

    ypred = np.array(model.predict(xtest))
    ytest = np.array(ytest)

    test_f1 = f1_score(ytest, ypred)
    test_precision = f1_score(ytest, ypred)

    dir, _ = opath.split(check_point_path)
    result_file = open(pjoin(dir, 'results.txt'), 'w')

    write = lambda val: print(val, file=result_file)
    write('accuracy, {0:1.6f}'.format(eval['accuracy']))
    write('recall@1, {0:1.6f}'.format(eval['recall@1']))
    write('recall@2, {0:1.6f}'.format(eval['recall@2']))
    write('precision, {0:1.6f}'.format(test_precision))
    write('f1, {0:1.6f}'.format(test_f1))
    write('')
    write('target_label, predicted_label, count')
    for row in eval['confusion_matrix']:
        write('{0}, {1}, {2}'.format(
            row['target_label'],
            row['predicted_label'],
            row['count']
        ))
    result_file.close()

    net.save(pjoin(dir, 'net.conf'))
