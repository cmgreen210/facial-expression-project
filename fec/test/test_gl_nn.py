import unittest
from fec.classifier.gl_nn import GraphLabNeuralNetBuilder


class GraphLabNeuralNetTest(unittest.TestCase):

    def test_convolution_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_convolution_layer(3, 1, 10)

        nn.add_convolution_layer(3, 1, 10, **{'padding': 1})

        return

    def test_max_pooling_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_max_pooling_layer(3)
        nn.add_max_pooling_layer(3, padding=0)
        nn.add_max_pooling_layer(3, 4, 5)

    def test_avg_pooling_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_avg_pooling_layer(3)
        nn.add_avg_pooling_layer(3, padding=0)
        nn.add_avg_pooling_layer(3, 4, 5)

    def test_flatten_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_flatten_layer()

    def test_full_connection_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_full_connection_layer(10)
        self.assertEqual(len(nn.layers), 2)
        self.assertEqual(nn.layers[0].name, 'flatten')

        nn = GraphLabNeuralNetBuilder()
        nn.add_avg_pooling_layer(3)
        nn.add_full_connection_layer(10)
        self.assertEqual(len(nn.layers), 3)

    def test_activation_layers(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_relu_layer()
        nn.add_sigmoid_layer()
        nn.add_tanh_layer()

    def test_drop_out_layer(self):
        nn = GraphLabNeuralNetBuilder()
        nn.add_dropout_layer()
        nn.add_dropout_layer(.8)
