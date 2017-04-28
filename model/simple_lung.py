import tensorflow as tf

x = tf.placeholder(tf.float32, [None,512*512])
W = tf.Variable(tf.zeros([512*512,2]))
b = tf.Variable(tf.zeros([2]))

y = tf.matmul(x,W) + b
y_ = tf.placeholder(tf.float32, [None,2])

