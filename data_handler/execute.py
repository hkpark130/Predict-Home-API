import pandas as pd
import numpy as np
import math
import tensorflow as tf

tf.reset_default_graph()

# TODO: data 값 받아오기
# data = np.array([[ ~ ]])

# 정규화를 위한 값
mean_arr = np.array([7.20945360e+00, 2.00915221e+03, 2.92888118e+00, 8.65568083e-01,
       3.58165655e+01, 1.00173461e-01, 1.95143105e-02, 9.93061578e-02,
       3.20901995e-02, 1.60450997e-02, 1.99479618e-02, 6.02775369e-02,
       1.60450997e-02, 8.28274068e-02, 2.64527320e-02, 5.50737207e-02,
       6.76496097e-02, 5.63746748e-02, 3.16565481e-02, 1.17085863e-02,
       4.50997398e-02, 3.51257589e-02, 3.25238508e-02, 6.02775369e-02,
       1.69124024e-02, 2.38508239e-02, 4.85689506e-02, 4.24978317e-02])
max_arr = np.array([  25, 2021,   21,    1,  187,    1,    1,    1,    1,    1,    1,
          1,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,
          1,    1,    1,    1,    1,    1])
mim_arr = np.array([   1, 1970,    1,    0,   15,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
          0,    0,    0,    0,    0,    0])
# data = (data - mean_arr) / (max_arr - mim_arr)

file = 'house'

x = tf.placeholder(tf.float32, [None,28])

L1 = tf.layers.dense(x, units=10, activation=tf.nn.relu, name=file+"L1")
L2 = tf.layers.dense(L1, units=10, activation=tf.nn.relu, name=file+"L2")
L3 = tf.layers.dense(L2, units=1, activation=None, name=file+"L3")

saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, '../learning_model/model/house-0') 

# Y_ = sess.run(L3, feed_dict={x:data})
# print( (Y_).astype(int)*1000 )