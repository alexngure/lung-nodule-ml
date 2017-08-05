from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

INPUT_SHAPE = 64,64

def lung_cnn(x):
    """A deep net that identifies nodules in a 2D patch of
    a lung image.
    """
    W_conv1 = weight_variable([3,3,1,32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x,W_conv1) + b_conv1)

    # downsample to 32x32
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([3,3,32,64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2) + b_conv2)

    # downsample to 16x16
    h_pool2 = max_pool_2x2(h_conv2)

    W_conv3 = weight_variable([3,3,64,128])
    b_conv3 = bias_variable([128])
    h_conv3 = tf.nn.relu(conv2d(h_pool2,W_conv2) + b_conv2)

    # downsample to 8x8
    h_pool3 = max_pool_2x2(h_conv3)

    W_conv4 = weight_variable([3,3,128,64])
    b_conv4 = bias_variable([64])
    h_conv4 = tf.nn.relu(conv2d(h_pool3,W_conv2) + b_conv2)

    # downsample to 4x4
    h_pool4 = max_pool_2x2(h_conv4)

    W_conv5 = weight_variable([3,3,64,32])
    b_conv5 = bias_variable([32])
    h_conv5 = tf.nn.relu(conv2d(h_pool4,W_conv2) + b_conv2)

    # downsample to 2x2
    h_pool5 = max_pool_2x2(h_conv5)

    W_conv6 = weight_variable([3,3,32,16])
    b_conv6 = bias_variable([16])
    h_conv6 = tf.nn.relu(conv2d(h_pool5,W_conv2) + b_conv2)

    # downsample to 1x1
    h_pool6 = max_pool_2x2(h_conv6)
    h_pool6_flat = tf.reshape([-1,16])

    W_fc1 = weight_variable([16,1024])
    b_fc1 = bias_variable([1024])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool6_flat,W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

    W_fc2 = weight_variable([1024,NUM_CLASSES])
    b_fc2 = bias_variable([NUM_CLASSES])

    y_conv = tf.matmul(h_fc1_drop,w_fc2) + b_fc2
    return y_conv

def conv2d(x, W):
  """conv2d returns a 2d convolution layer with full stride.

  source: tensorflow/deep_mnist.py
  """
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  """max_pool_2x2 downsamples a feature map by 2X.

  source: tensorflow/deep_mnist.py
  """
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  """weight_variable generates a weight variable of a given shape.

  source: tensorflow/deep_mnist.py
  """
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  """bias_variable generates a bias variable of a given shape.

  source: tensorflow/deep_mnist.py
  """
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)
  
