import sys
import os
import json
import tornado.escape
import numpy as np;
import math
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.pardir)
tf.compat.v1.disable_eager_execution()

class HouseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS,POST')

    def get(self):
        data={}
        try:
            header= self.request.headers.get('data')
            data = json.loads(header)
        except:
            _, ms, _ = sys.exc_info()
            message = "Error Message:{0}".format(ms)
            self.write(message)
        try:
            # TODO:파라미터 넘겨서 집 값 예측
            param_arr = np.zeros(shape=(28,), dtype=np.int64)
            param_arr[0] = data['dis_to_station']   # 역까지 거리
            param_arr[1] = data['year_of_cons']     # 건축년도
            param_arr[2] = data['floors']           # 층수
            param_arr[3] = data['separ_toilet']     # 욕실 화장실 분리
            param_arr[4] = data['area']             # 면적
            param_arr[int(data['address'])+5] = 1   # 주소
            param_arr = [param_arr]

            mean_arr = np.array(os.getenv('MEAN').split(',')).astype(float)
            max_arr = np.array(os.getenv('MAX').split(',')).astype(float)
            mim_arr = np.array(os.getenv('MIN').split(',')).astype(float)
            param_arr = (param_arr - mean_arr) / (max_arr - mim_arr)

            file = 'house'
            with tf.compat.v1.variable_scope(file, reuse=tf.compat.v1.AUTO_REUSE) as scope:
                x = tf.compat.v1.placeholder(tf.float32, [None,28])

                L1 = tf.compat.v1.layers.dense(x, units=10, activation=tf.nn.relu, name=file+"L1")
                L2 = tf.compat.v1.layers.dense(L1, units=10, activation=tf.nn.relu, name=file+"L2")
                L3 = tf.compat.v1.layers.dense(L2, units=1, activation=None, name=file+"L3")

                saver = tf.compat.v1.train.Saver()
                sess = tf.compat.v1.Session()
                saver.restore(sess, './learning_model/model/'+file + '.ckpt-0') 

                Y_ = sess.run(L3, feed_dict={x:param_arr})

            output = str( int(Y_[0][0])*1000 )
            self.write(output)
        except:
            _, ms, _ = sys.exc_info()
            message = "Error Message:{0}".format(ms)
            self.write(message)
            pass
