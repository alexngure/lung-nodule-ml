import tensorflow as tf
from DataManager import DataLoader

x = tf.placeholder(tf.float32, [None,512*512])
W = tf.Variable(tf.zeros([512*512,2]))
b = tf.Variable(tf.zeros([2]))

y = tf.matmul(x,W) + b
y_ = tf.placeholder(tf.float32, [None,2])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.nn.GradientDescentOptimizer(0.5).minimize(cross_entropy)
correct_prediction = tf.equal(tf.arg_max(y,1),tf.arg_max(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

iterations = 5000
batch_size = 10

data = DataLoader('../data/training_set_raw.data')

with tf.Session() as sesh:
    sesh.run(tf.global_variables_initializer().run())
    for _ in range(iterations):
        batch_xs,batch_ys = data.next_batch(batch_size)
        if i%100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x:batch_xs,y_:batch_ys})
            print('Step %d, training accuracy %g'(i,train_accuracy))
        train_step.run(feed_dict={x:batch_xs,y_:batch_ys})
    print('test accuracy %g'%accuracy.eval(feed_dict={x:data.test_images, y_:data.test_labels}))
