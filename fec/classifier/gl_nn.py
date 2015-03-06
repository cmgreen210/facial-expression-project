import graphlab as gl


class GraphLabNeuralNet(object):
    def __init__(self):
        self.layers = list()

    def add_convolution_layer(self, kernel_size,
                              stride, num_channels, **kwargs):
        conv_layer = gl.deeplearning.layers.ConvolutionLayer(
            kernel_size=kernel_size, num_channels=num_channels,
            stride=stride, **kwargs
        )
        self.layers.append(conv_layer)