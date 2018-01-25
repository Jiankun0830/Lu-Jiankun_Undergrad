import timeit
import numpy
import tensorflow as tf

from tf_neural_net import policy_value_net
#from my_freeze_graph import freeze_graph
#from test_model import run_test

numInputChannels = 17
numFiles = 19

def read_and_decode(filename):
    # x: input, y: next move, z: result of game
    features = tf.parse_single_example(
        filename,
        features={
            'x_raw': tf.FixedLenFeature([], tf.string),
            'y_raw': tf.FixedLenFeature([], tf.string),
            'z_raw': tf.FixedLenFeature([], tf.string)
    })
    
    x_processed = tf.reshape(tf.decode_raw(features['x_raw'], tf.float32), (19, 19, numInputChannels))
    y_processed = tf.reshape(tf.decode_raw(features['y_raw'], tf.int32), ())
    z_processed = tf.reshape(tf.decode_raw(features['z_raw'], tf.int32), ())
    
    return x_processed, y_processed, z_processed

# Build graph
print('Building graph ...')

filenames = ['D:\\Training data\\zero_data' + str(x) + '.tfrecords' for x in range(1, numFiles + 1)]
dataset = tf.contrib.data.TFRecordDataset(filenames)
dataset = dataset.map(read_and_decode)
dataset = dataset.batch(32)

test_filename = 'D:\\Training data\\zero_data20.tfrecords'
test_dataset = tf.contrib.data.TFRecordDataset(test_filename)
test_dataset = test_dataset.map(read_and_decode)
test_dataset = test_dataset.batch(4096)

iterator = tf.contrib.data.Iterator.from_structure(dataset.output_types, dataset.output_shapes)

training_init_op = iterator.make_initializer(dataset)
test_init_op = iterator.make_initializer(test_dataset)

#iterator = dataset.make_initializable_iterator()

x_batch, y_batch, z_batch = iterator.get_next()
phase = tf.placeholder(tf.bool, name='phase')

# number of filters
k = 32 

policy_output, value_output = policy_value_net(x_batch, numInputChannels, k, phase)

y_onehot = tf.one_hot(y_batch, 362, dtype=tf.int32)

# mse_loss = tf.losses.mean_squared_error(labels=tf.cast(y_batch, tf.float32), predictions=value_output)

loss = -tf.reduce_mean(tf.log(tf.reduce_sum(tf.to_float(y_onehot) * policy_output, reduction_indices=[1])))

tf.summary.scalar('loss', loss)

# Training
print('Training ...')

#cross_entropy = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(y_output, y_batch))

train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

y_pred = tf.argmax(policy_output, 1)
y_actual = tf.cast(y_batch, tf.int64)

correct_prediction = tf.equal(y_pred, y_actual)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

count = 0

init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer(), name="init_node")

#all_saver = tf.train.Saver([W_conv0, W_conv1, W_conv2, b_conv0, b_conv1, b_conv2])
all_saver = tf.train.Saver()



with tf.Session() as sess:
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter('log/', sess.graph)
    
    sess.run(init_op)

    sess.run(training_init_op)
    #sess.run(iterator.initializer)    

    start_time = timeit.default_timer()

    flag = True

    while flag:
        try:
            _, acc, ls, yp, ya, summary = sess.run([train_op, accuracy, loss, y_pred, y_actual, merged], feed_dict={'phase:0': 1})
            count = count + 1

            train_writer.add_summary(summary, count)
            
            if count % 256 == 0:
                print(count)
                print(ls)
                print(yp)
                print(ya)
                print(acc) 

        except tf.errors.OutOfRangeError:
            end_time = timeit.default_timer()     

            flag = False
            print('Optimization complete.')          
            print(('Training ran for %.2fm') % ((end_time - start_time) / 60.))

            #all_saver.save(sess, 'models/nic24k64_model.ckpt')
            #freeze_graph('nic24k64_model.ckpt', 'nic24k64_graph_deploy.pb')
            #run_test('nic24k64_graph_deploy.pb')


    sess.run(test_init_op)

    start_time = timeit.default_timer()
    flag = True

    while flag:
        try:
            acc = sess.run(accuracy, feed_dict={'phase:0': 0})
            
        except tf.errors.OutOfRangeError:
            end_time = timeit.default_timer()     

            flag = False
            print(acc)
            print(('Testing ran for %.2fm') % ((end_time - start_time) / 60.))