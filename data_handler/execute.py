import pandas as pd
import numpy as np
import math
import tensorflow as tf

tf.reset_default_graph()

# TODO: data 값 받아오기
#data = 

x = tf.placeholder(tf.float32, [None,28])

L1 = tf.layers.dense(x, units=10, activation=tf.nn.relu)
L2 = tf.layers.dense(L1, units=10, activation=tf.nn.relu)
L3 = tf.layers.dense(L2, units=1, activation=None)

saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, '../learning_model/model/house-0') 

# Y_ = sess.run(L3, feed_dict={x:data})
# print((Y_*1000).astype(int))