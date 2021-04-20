import pandas as pd
import numpy as np
import math
import tensorflow as tf

tf.reset_default_graph()

# 도쿄 23구 csv 넣기
df_house = pd.read_csv('../scraping/house.csv', sep='\t', encoding='utf-8')
df = pd.concat([
                df_house
               ], axis=0, ignore_index=True)

# 불필요 칼럼 제거
df.drop(['Unnamed: 0'], axis=1, inplace=True)
df['住所'] = df['住所'].str.replace(u'丁目', u'') # 丁目는 공통으로 있으니 지우기
df['賃料'] = (df['賃料'] / 1000).astype(int) # 야칭 편차 줄이기

# 주소 더미화
dummies_address = pd.get_dummies(df['住所'])
df = pd.concat([df, dummies_address], axis=1)
df.drop(['住所'], inplace=True, axis=1)

# 집 값 데이터는 기댓값(Y)으로 빼주기
Y = np.array(df['賃料']).reshape(-1,1)
df.drop(['賃料'], axis=1, inplace=True)

# 학습 데이터(X) 정규화
df = (df - df.mean()) / (df.max() - df.min())
data = np.array(df)
X = data

#---여기까지는 학습을 위한 데이터 정제 작업---
x = tf.placeholder(tf.float32, [None,28])
y = tf.placeholder(tf.float32, [None,1])

file = 'house'
# TODO: (학습데이터 80%)/(검증 데이터 20%) 나누어야 함 (지금은 적용 안된 거)
# dense 신경망 모델로 학습 (이 부분부터는 무슨 모델이 정답인지 모르겠습니다. 여러 모델로 시도해봐주세요)
L1 = tf.layers.dense(x, units=10, activation=tf.nn.relu, name=file+"L1")
L2 = tf.layers.dense(L1, units=10, activation=tf.nn.relu, name=file+"L2")
L3 = tf.layers.dense(L2, units=1, activation=None, name=file+"L3")
loss = tf.reduce_mean( 0.5*tf.square(L3-y) )
train = tf.train.AdamOptimizer(0.1).minimize(loss)
saver = tf.train.Saver()

# 학습 실행
sess = tf.Session()
sess.run(tf.global_variables_initializer())
for j in range(50000):
    loss_, _ = sess.run([loss, train], feed_dict={x: X, y: Y})
    
# 학습 결과
print("loss값 : {}".format(loss_) )
# loss 값이 적을수록 좋은데, 고성능의 컴퓨터일수록 결과가 좋게 나왔음
saver.save(sess, './model/' + file, global_step=0)  # 모델 저장

# 학습 모델 테스트
test = df[0:5]
Y_ = sess.run(L3, feed_dict={x:test})
print((Y_*1000).astype(int)) # 円 (예측 집 값)