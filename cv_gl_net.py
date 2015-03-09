import graphlab as gl
from fec.classifier.gl_nn import GraphLabNeuralNetBuilder
from fec.classifier.gl_classifier import GraphLabClassifierFromNetBuilder
import pandas as pd
import numpy as np


# Create network builder and set network parameters
net = GraphLabNeuralNetBuilder()
net['learning_rate'] = 0.05
net['momentum'] = 0.7
net['divideby'] = 255
net['learning_rate_schedule'] = 'polynomial_decay'
net['batch_size'] = 256
net['learning_rate_alpha'] = 1
net['learning_rate_gamma'] = 5e-5


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

df = pd.read_pickle('/home/ec2-user/data/fer_data.pkl')
x = np.array(df['pixels'].tolist())
y = np.array(df['emotion'].values)

model = GraphLabClassifierFromNetBuilder(net, chkpt_dir=check_point_path,
                                         max_iterations=20000, train_frac=.9)
model.fit(x, y)
# cv = 1
#
# for i in xrange(5):
#     check_point = check_point_path.format(i+1)
#     train, _ = training_data.random_split(.8)
#     model = gl.neuralnet_classifier.create(
#         train,
#         target=target,
#         max_iterations=max_iterations,
#         network=network,
#         model_checkpoint_path=check_point,
#         validation_set=test_data,
#         verbose=True
#     )
