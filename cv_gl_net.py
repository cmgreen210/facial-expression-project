import graphlab as gl
from fec.classifier.gl_nn import GraphLabNeuralNetBuilder

# Create network builder and set network parameters
net = GraphLabNeuralNetBuilder()
net['learning_rate'] = 0.05
net['momentum'] = 0.9
net['subtract_mean'] = True
net['divideby'] = 255
net['random_mirror'] = True
net['learning_rate_schedule'] = 'polynomial_decay'
net['batch_size'] = 256

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


check_point_path = "/home/ec2-user/chkpts/cv/{0}"
data_frame_path = "/home/ec2-user/data/graphlab-35k/"

data = gl.load_sframe(data_frame_path)

cv = 5

max_iterations = 200
target = 'label'
network = net.get_net()
verbose = True

training_data, test_data = data.random_split(.8)

for i in xrange(5):
    check_point = check_point_path.format(i+1)
    train, _ = training_data.random_split(.8)
    model = gl.neuralnet_classifier.create(
        train,
        target=target,
        max_iterations=max_iterations,
        network=network,
        model_checkpoint_path=check_point,
        validation_set=test_data,
        verbose=True
    )
