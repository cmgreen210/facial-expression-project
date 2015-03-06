import graphlab as gl


class GraphLabNeuralNetBuilder(object):
    def __init__(self):
        self.layers = list()
        self.net = gl.deeplearning.NeuralNet()

    def get_net(self):
        self.net.layers = self.layers
        self.net.verify()
        return self.net

    def verify(self):
        self.net.layers = self.layers
        return self.net.verify()

    def add_convolution_layer(self, kernel_size,
                              stride, num_channels, **kwargs):
        conv_layer = gl.deeplearning.layers.ConvolutionLayer(
            kernel_size=kernel_size, num_channels=num_channels,
            stride=stride, **kwargs
        )
        self.layers.append(conv_layer)
        return

    def add_max_pooling_layer(self, kernel_size, stride=1, padding=0):
        pool_layer = gl.deeplearning.layers.MaxPoolingLayer(
            kernel_size=kernel_size, stride=stride, padding=padding
        )
        self.layers.append(pool_layer)
        return

    def add_avg_pooling_layer(self, kernel_size, stride=1, padding=0):
        pool_layer = gl.deeplearning.layers.AveragePoolingLayer(
            kernel_size=kernel_size, stride=stride, padding=padding
        )
        self.layers.append(pool_layer)
        return

    def add_flatten_layer(self):
        self.layers.append(
            gl.deeplearning.layers.FlattenLayer()
        )
        return

    def add_full_connection_layer(self, num_hidden_units,
                                  init_bias=0, init_sigma=0.01,
                                  init_random='gaussian'):
        fc_layer = gl.deeplearning.layers.FullConnectionLayer(
            num_hidden_units, init_bias=init_bias, init_sigma=init_sigma,
            init_random=init_random
        )
        self.layers.append(fc_layer)
        return

    def add_relu_layer(self):
        self.layers.append(gl.deeplearning.layers.RectifiedLinearLayer())
        return

    def add_sigmoid_layer(self):
        self.layers.append(gl.deeplearning.layers.SigmoidLayer())

    def add_tanh_layer(self):
        self.layers.append(gl.deeplearning.layers.TanhLayer())

    def add_soft_plus_layer(self):
        self.layers.append(gl.deeplearning.layers.SoftplusLayer())

    def add_soft_max_layer(self):
        self.layers.append(gl.deeplearning.layers.SoftmaxLayer())

    def add_dropout_layer(self, threshold=0.5):
        drop_layer = gl.deeplearning.layers.DropoutLayer(threshold)
        self.layers.append(drop_layer)

    def __getitem__(self, item):
        return self.net.params[item]

    def __setitem__(self, key, value):
        self.net.params[key] = value
