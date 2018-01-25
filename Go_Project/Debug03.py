import tensorflow as tf
import numpy

from tf_neural_net import policy_value_net

N = 19
batch_size = 1
numInputChannels = 2
k= 16

init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer(), name="init_node")

board_input = tf.placeholder(tf.float32, shape=(batch_size, N, N, numInputChannels))
gen_phase = tf.placeholder(tf.bool)
nn_output = policy_value_net(board_input, numInputChannels, k, gen_phase)

sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
sess.run(tf.global_variables_initializer())

input_batch = numpy.zeros((batch_size, N, N, numInputChannels))

p, v = sess.run(nn_output, feed_dict={board_input: input_batch, gen_phase: 0})