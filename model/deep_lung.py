from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import numpy as np
import os
import random
import tensorflow as tf

random.seed(10)

log_dir          = r'logs'
positive_ex_path = r'lidc_positive.npy'
negative_ex_path = r'lidc_negative.npy'
positive_exs     = np.load(positive_ex_path,mmap_mode='r')
negative_exs     = np.load(negative_ex_path,mmap_mode='r')

NUM_POSITIVE     = positive_exs.shape[0]
NUM_NEGATIVE     = negative_exs.shape[0]
TEST_PERCENT     = 0.1
POS_TEST         = int(NUM_POSITIVE*TEST_PERCENT)
NEG_TEST         = int(NUM_NEGATIVE*TEST_PERCENT)
POS_TRAIN        = NUM_POSITIVE - POS_TEST
NEG_TRAIN        = NUM_NEGATIVE - NEG_TEST
TRAIN_POS_RANGE  = (0,POS_TRAIN-1)
TRAIN_NEG_RANGE  = (0,NEG_TRAIN-1)
TEST_POS_RANGE   = (POS_TEST,NUM_POSITIVE-1)
TEST_NEG_RANGE   = (NEG_TEST,NUM_NEGATIVE-1)
INPUT_SHAPE      = 64,64
PIXEL_COUNT      = INPUT_SHAPE[0]*INPUT_SHAPE[1]
NUM_CLASSES      = 2
LR               = 0.01
ITER             = 150001
T_STEPS          = 100
SAVE_STEPS       = 10000
BATCH_SIZE       = 20
TEST_SIZE        = 600

def lung_cnn(x):
    """A deep net that identifies nodules in a 2D patch of
    a lung image.
    """
    x_image = tf.reshape(x,[-1,INPUT_SHAPE[0],INPUT_SHAPE[1],1])
    W_conv1 = weight_variable([3,3,1,64],name='W_conv1')
    b_conv1 = bias_variable([64],name='b_conv1')
    h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1) + b_conv1)

    # downsample to 32x32
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([3,3,64,128],name='W_conv2')
    b_conv2 = bias_variable([128],name='b_conv2')
    h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2) + b_conv2)

    # downsample to 16x16
    h_pool2 = max_pool_2x2(h_conv2)

    W_conv3 = weight_variable([3,3,128,256],name='W_conv3')
    b_conv3 = bias_variable([256],name='b_conv3')
    h_conv3 = tf.nn.relu(conv2d(h_pool2,W_conv3) + b_conv3)

    # downsample to 8x8
    h_pool3 = max_pool_2x2(h_conv3)

    W_conv4 = weight_variable([3,3,256,128],name='W_conv4')
    b_conv4 = bias_variable([128],name='b_conv4')
    h_conv4 = tf.nn.relu(conv2d(h_pool3,W_conv4) + b_conv4)

    # downsample to 4x4
    h_pool4 = max_pool_2x2(h_conv4)

    W_conv5 = weight_variable([3,3,128,64],name='W_conv5')
    b_conv5 = bias_variable([64],name='b_conv5')
    h_conv5 = tf.nn.relu(conv2d(h_pool4,W_conv5) + b_conv5)

    # downsample to 2x2
    h_pool5 = max_pool_2x2(h_conv5)

    W_conv6 = weight_variable([3,3,64,32],name='W_conv6')
    b_conv6 = bias_variable([32],name='b_conv6')
    h_conv6 = tf.nn.relu(conv2d(h_pool5,W_conv6) + b_conv6)

    # downsample to 1x1
    h_pool6 = max_pool_2x2(h_conv6)
    h_pool6_flat = tf.reshape(h_pool6,[-1,32])

    W_fc1 = weight_variable([32,1024],name='W_fc1')
    b_fc1 = bias_variable([1024],name='b_fc1')
    h_fc1 = tf.nn.relu(tf.matmul(h_pool6_flat,W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

    W_fc2 = weight_variable([1024,NUM_CLASSES],name='W_fc2')
    b_fc2 = bias_variable([NUM_CLASSES],name='b_fc2')

    y_conv = tf.matmul(h_fc1_drop,W_fc2) + b_fc2
    return y_conv,keep_prob

def conv2d(x, W,strides=[1,1,1,1]):
    """conv2d returns a 2d convolution layer with specified stride."""
    return tf.nn.conv2d(x, W, strides=strides, padding='SAME')


def max_pool_2x2(x,strides=[1,2,2,1]):
    """max_pool_2x2 downsamples a feature map by 2X."""
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=strides, padding='SAME')


def weight_variable(shape,name):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial,name=name)


def bias_variable(shape,name):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial,name=name)

def load_example(ex):
    """ex is a list of the form [image_path,image_uid]. load_example
    opens the image, creates patches, and assigns a positive label
    to patches with nodule pixels.
    """
    return

def generate_batch(batch_size):
    """Loads and returns a minibatch of size 'batch_size.'"""
    return

def generate_test_batch(batch_size):
    """Loads and returns the test set."""
    return