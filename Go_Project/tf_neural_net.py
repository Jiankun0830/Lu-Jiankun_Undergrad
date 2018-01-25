import tensorflow as tf
import numpy

def policy_value_net(input, numInputChannels, k, phase):
    layer_0_output = conv4Layer(input, numInputChannels, k, 5, layer_num=0, phase=phase)

   # layer_1_output = G4Layer(layer_0_output, k, k, 3, layer_num=1, phase=phase)
   # layer_2_output = G4Layer(layer_1_output, k, k, 3, layer_num=2, phase=phase)
   # layer_3_output = G4Layer(layer_2_output, k, k, 3, layer_num=3, phase=phase)
   # layer_4_output = G4Layer(layer_3_output, k, k, 3, layer_num=4, phase=phase)
   # layer_5_output = G4Layer(layer_4_output, k, k, 3, layer_num=5, phase=phase)
   # layer_6_output = G4Layer(layer_5_output, k, k, 3, layer_num=6, phase=phase)
   # layer_7_output = G4Layer(layer_6_output, k, k, 3, layer_num=7, phase=phase)
    layer_8_output = G4Layer(layer_0_output, k, k, 3, layer_num=8, phase=phase)
    layer_9_output = G4Layer(layer_8_output, k, k, 3, layer_num=9, phase=phase)
    layer_10_output = G4Layer(layer_9_output, k, k, 3, layer_num=10, phase=phase)
    layer_11_output = G4Layer(layer_10_output, k, 4, 3, layer_num=11, phase=phase)

    # value head
    # sum over rotations for invariance, then apply fully-connected layers
    inv_output = tf.reshape(layer_11_output[:,:,:,0] + tf.transpose(layer_11_output[:,:,:,1], [0, 2, 1])[:,::-1,:] + layer_11_output[:,:,:,2][:,:,::-1][:,::-1,:] 
                    + tf.transpose(layer_11_output[:,:,:,3], [0, 2, 1])[:,:,::-1], [-1, 361])

    hidden_layer_output = hidden_layer(inv_output, 361, 256, phase=phase)

    value_output = tf.reshape(tanh_layer(hidden_layer_output, 256, 1, phase=phase), [-1])

    # policy head
    equiv_output = tf.reshape(tf.reduce_mean(layer_11_output, 3), [-1, 361], name="flatten")

    softmax_output = tf.nn.softmax(hidden_layer(equiv_output, 361, 362, phase=phase), name="softmax_node")

    policy_output = tf.div(softmax_output, tf.reduce_sum(softmax_output, 1, keep_dims=True), name="policy_output_node")    
    
    return policy_output, value_output


def conv_orig(input, n_in, n_out, window_size, layer_num, phase):
    W = tf.Variable(tf.truncated_normal([window_size, window_size, n_in, n_out], stddev=0.05), name="W" + str(layer_num))
    #b = tf.Variable(tf.zeros([n_out]), name="b" + str(layer_num))

    conv = tf.nn.conv2d(input, W, strides=[1, 1, 1, 1], padding='SAME')

    h1 = tf.contrib.layers.batch_norm(conv, center=True, scale=True, is_training=phase)

    return tf.nn.relu(h1)

def tanh_layer(input, n_in, n_out, phase):
    W = tf.Variable(tf.truncated_normal([n_in, n_out], stddev=0.0625), name="tanhL_W")
    #b = tf.Variable(tf.zeros([n_out]), name="tanhL_b")

    h1 = tf.contrib.layers.batch_norm(tf.matmul(input, W), center=True, scale=True, is_training=phase)

    return tf.tanh(h1)
    #return tf.sigmoid(tf.matmul(input, W) + b)
  


def hidden_layer(input, n_in, n_out, phase):
    W = tf.Variable(tf.truncated_normal([n_in, n_out], stddev=0.05), name="h_W")
    #b = tf.Variable(tf.zeros([n_out]), name="h_b")

    h1 = tf.contrib.layers.batch_norm(tf.matmul(input, W), center=True, scale=True, is_training=phase)

    return tf.nn.relu(h1)


def conv4Layer(input, n_in, n_out, window_size, layer_num, phase):
    W = tf.Variable(tf.truncated_normal([window_size, window_size, n_in, int(n_out/4)], stddev=0.15), name="W" + str(layer_num))    
    #b = tf.Variable(tf.constant(0.0, shape=[n_out]), name="b" + str(layer_num))

    conv_outE = tf.nn.conv2d(input, W, strides=[1, 1, 1, 1], padding='SAME')
    conv_out90 = tf.nn.conv2d(input, tf.transpose(W, [1, 0, 2, 3])[:,::-1,:,:], strides=[1, 1, 1, 1], padding='SAME')
    conv_out180 = tf.nn.conv2d(input, W[::-1,:,:,:][:,::-1,:,:], strides=[1, 1, 1, 1], padding='SAME')
    conv_out270 = tf.nn.conv2d(input, tf.transpose(W, [1, 0, 2, 3])[::-1,:,:,:], strides=[1, 1, 1, 1], padding='SAME')

    h1 = tf.contrib.layers.batch_norm(tf.concat([conv_outE, conv_out90, conv_out180, conv_out270], 3), center=True, scale=True, is_training=phase)

    return tf.nn.relu(h1)


def G4Layer(input, n_in, n_out, window_size, layer_num, phase):
    W = tf.Variable(tf.truncated_normal([4, window_size, window_size, int(n_in/4), int(n_out/4)], stddev=0.15), name="W" + str(layer_num))    
    b = tf.Variable(tf.constant(0.0, shape=[n_out]), name="b" + str(layer_num))

    WE = tf.concat([W[0], tf.transpose(W[3], [1, 0, 2, 3])[:,::-1,:,:], W[2][::-1,:,:,:][:,::-1,:,:], tf.transpose(W[1], [1, 0, 2, 3])[::-1,:,:,:]], 2)
    OE_conv = tf.nn.conv2d(input, WE, strides=[1, 1, 1, 1], padding='SAME')

    W90 = tf.concat([W[1], tf.transpose(W[0], [1, 0, 2, 3])[:,::-1,:,:], W[3][::-1,:,:,:][:,::-1,:,:], tf.transpose(W[2], [1, 0, 2, 3])[::-1,:,:,:]], 2)
    O90_conv = tf.nn.conv2d(input, W90, strides=[1, 1, 1, 1], padding='SAME')

    W180 = tf.concat([W[2], tf.transpose(W[1], [1, 0, 2, 3])[:,::-1,:,:], W[0][::-1,:,:,:][:,::-1,:,:], tf.transpose(W[3], [1, 0, 2, 3])[::-1,:,:,:]], 2)
    O180_conv = tf.nn.conv2d(input, W180, strides=[1, 1, 1, 1], padding='SAME')

    W270 = tf.concat([W[3], tf.transpose(W[2], [1, 0, 2, 3])[:,::-1,:,:], W[1][::-1,:,:,:][:,::-1,:,:], tf.transpose(W[0], [1, 0, 2, 3])[::-1,:,:,:]], 2)
    O270_conv = tf.nn.conv2d(input, W270, strides=[1, 1, 1, 1], padding='SAME')

    h1 = tf.contrib.layers.batch_norm(tf.concat([OE_conv, O90_conv, O180_conv, O270_conv], 3), center=True, scale=True, is_training=phase)

    return tf.nn.relu(h1)

