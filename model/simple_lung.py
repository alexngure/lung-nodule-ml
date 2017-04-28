import tensorflow as tf

x = tf.placeholder(tf.float32, [None,512*512])
W = tf.Variable(tf.zeros([512*512,2]))
b = tf.Variable(tf.zeros([2]))
