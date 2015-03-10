import graphlab as gl
from fec.classifier.gl_nn import GraphLabNeuralNetBuilder
from fec.classifier.gl_classifier import GraphLabClassifierFromNetBuilder
import pandas as pd
import numpy as np
import sys
from sklearn.cross_validation import train_test_split


def create_gl_default(net, conv_channels=10, hidden_channels=100):
    #   ----Conv
    stride = 1
    num_channels = conv_channels
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
    num_hidden_units = hidden_channels

    net.add_full_connection_layer(num_hidden_units)

    #----ReLu-------
    net.add_relu_layer()

    #----Drop Out----
    threshold = 0.5
    net.add_dropout_layer(threshold=0.5)

    #-----Fully Connected-----
    num_hidden_units = 7

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
        net = create_net_kag(net)
    elif model == 2:
        net = create_gl_default(net)
    elif model == 3:
        net = create_gl_default(net, 32)
    else:
        exit()

    df = pd.read_pickle(data_path)
    x = np.array(df['pixels'].tolist())
    y = np.array(df['emotion'].values)

    xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=.9)

    model = GraphLabClassifierFromNetBuilder(net, chkpt_dir=check_point_path,
                                             max_iterations=max_iterations,
                                             train_frac=.91)
    model.fit(xtrain, ytrain)

    print model.evaluate(xtest, ytest, metric=['accuracy', 'confusion_matrix',
                                               'recall@1', 'recall@2'])
