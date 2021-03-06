from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

# MNIST数据存放路径
file = "./data" 

# 导入数据
mnist = input_data.read_data_sets(file,one_hot=True)

# 模型的输入和输出
x = tf.placeholder(tf.float32,shape=[None,784])
y_= tf.placeholder(tf.float32,shape=[None,10])

# # 模型的权重和偏移量
# W = tf.Variable(tf.zeros([784,10]))
# b = tf.Variable(tf.zeros([10]))


# 创建Session
sess = tf.InteractiveSession()

# # 初始化权重变量
# sess.run(tf.initialize_all_variables)

# # 构建回归模型
# y = tf.nn.softmax(tf.matmul(x,W)+b)

# # 交叉熵
# cross_entropy = -tf.reduce_sum(y_*tf.log(y))

# #训练
# train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
# for i in range(1000):
#     batch = mnist.train.next_batch(50)
#     train_step.run(feed_dict={x:batch[0],y_:batch[1]})

# # 测试
# # 这里返回一个布尔数组，形如[True, False, True]
# correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
# # 将布尔数组转换为浮点数，并取平均值，如上布尔数组可以转换为[1, 0, 1]，计算平均值为0.667
# accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
# # 计算在测试数据上的准确率
# print(sess.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))


def weigth_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#第一层卷积
W_conv1 = weigth_variable([5,5,1,32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x,[-1,28,28,1])

h_conv1 = tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

#第二层卷积
W_conv2 = weigth_variable([5,5,32,64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

#密集连接层
W_fc1 = weigth_variable([7*7*64,1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2,[-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)

#Dropout
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1,keep_prob)

#输出层
W_fc2 = weigth_variable([1024,10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

#训练与评估
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
sess.run(tf.initialize_all_variables())
for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        train_accuray = accuracy.eval(feed_dict={x:batch[0],y_:batch[1],keep_prob:1.0})
        print("stpe %d,training accuracy %g"%(i,train_accuray))
    train_step.run(feed_dict={x:batch[0],y_:batch[1],keep_prob:0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={x:mnist.test.images,y_:mnist.test.labels,keep_prob:1.0}))


