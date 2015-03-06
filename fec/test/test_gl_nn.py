import unittest
from fec.classifier.gl_nn import GraphLabNeuralNet


class GraphLabNeuralNetTest(unittest.TestCase):

    def test_convolution_layer(self):
        nn = GraphLabNeuralNet()
        nn.add_convolution_layer(3, 1, 10)

        nn.add_convolution_layer(3, 1, 10, **{'padding': 1})

        return
