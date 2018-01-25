import numpy
import tensorflow as tf
import operator
import math
import sys
import time
import timeit
import threading

from game_state import board_state_to_numpy_arr, process_input, empty_position
from tf_neural_net import policy_value_net

numInputChannels = 2
k = 32

N = 7
W = N + 2
colstr = 'ABCDEFGHJKLMNOPQRST'
MAX_GAME_LEN = N*N*2

def best_move(probs):    
    return numpy.argmax(probs)

def numpy_ind_to_gs_ind(ind):
    if ind == N*N:
        return None
    else:        
        row = ind // N
        col = ind % N
        return W + 1 + (row * W) + col

def gs_ind_to_numpy_ind(ind):
    if ind == None:
        return N*N
    else:    
        row, col = divmod(ind - (W+1), W)
        return row*N + col

def gen_playout_moves(myboard, prob_vector):    
    actions = [] # all possible moves
    
    for i in myboard.moves(0):
        newboard = myboard
        if newboard.move(i) is not None:
            actions.append(i)
    
    for ind in actions:
        yield (ind, prob_vector[gs_ind_to_numpy_ind(ind)])

    yield(-1, prob_vector[N*N])

class TreeNode():
    """ Monte-Carlo tree node;
    v is #visits, w is #wins for to-play (expected reward is w/v)
    children is None for leaf nodes """
    def __init__(self, pos):
        self.pos = pos
        self.v = 0
        self.w = 0
        self.pb = 0.0    
        self.value = 0.5
        self.children = None   

    def winrate(self):
        return float(self.w) / self.v if self.v > 0 else float('nan')

    def best_move(self):
        """ best move is the most simulated one """
        return max(self.children, key=lambda node: node.v) if self.children is not None else None

def expand_node(node, prob_vector):
    node.children = []
      
    for ind, prob in gen_playout_moves(node.pos, prob_vector):
        if ind == -1:
            c_pos = node.pos.pass_move()
        else:
            c_pos = node.pos.move(ind)

        if c_pos is None:
            continue

        c_node = TreeNode(c_pos)
        c_node.pb = prob
        node.children.append(c_node)           
    

def tree_descend(root_node, disp=False):
    """ Descend through the tree to a leaf """
    root_node.v += 1
    nodes_list = [root_node]
    passes = 0

    cur_node = root_node

    while cur_node.children is not None and passes < 2:
        #if disp:  
          #  print_pos(cur_node.pos)

        # Pick the most urgent child
        children = list(cur_node.children)

        #if disp:
         #   for c in children:
           #     dump_subtree(c, recurse=False)
        
        cur_node = max(children, key=lambda c: (float(c.w) / (1 + c.v)) + c.pb * math.sqrt(5.0 * math.log(1 + cur_node.v) / (1 + c.v)))

        nodes_list.append(cur_node)

        #if disp:  
           # print('chosen %s' % (str_coord(cur_node.pos.last),), file=sys.stderr)

        if cur_node.pos.last is None:
            passes += 1
        else:
            passes = 0           

        # updating visits on the way *down* represents "virtual loss", relevant for parallelization
        cur_node.v += 1      

    return nodes_list


def tree_update(nodes, score, disp=False):
    """ Store simulation result in the tree (@nodes is the tree path) """
    for node in reversed(nodes):
        #if disp:  
          #  print('updating', str_coord(node.pos.last), score < 0, file=sys.stderr)
       
        node.w += score < 0  # score is for to-play, node statistics for just-played
               
        if node.children is not None:
            for child in node.children:
                if child.pos.last is None:
                    continue

        score = -score

def str_coord(c):
    if c is None:
        return 'pass'
    row, col = divmod(c - (W+1), W)
    return '%c%d' % (colstr[col], N - row)

def print_tree_summary(tree, sims, f=sys.stderr):
    best_nodes = sorted(tree.children, key=lambda n: n.v, reverse=True)[:5]
    best_seq = []
    node = tree
    while node is not None:
        best_seq.append(node.pos.last)
        node = node.best_move()
    print('[%4d] winrate %.3f | seq %s | can %s' %
          (sims, best_nodes[0].winrate(), ' '.join([str_coord(c) for c in best_seq[1:6]]),
           ' '.join(['%s(%.3f)' % (str_coord(n.pos.last), n.winrate()) for n in best_nodes])), file=f)


def search_policy(node, temp=1):
    output = numpy.zeros(N*N + 1)

    for c in node.children:
        # print(c.pos.last)
        # print(c.v)
        ind = gs_ind_to_numpy_ind(c.pos.last)

        output[ind] = c.v ** (1/temp)

    return output/numpy.sum(output)

### sample from probability vector
def weight_sample(probs): 
    rad = numpy.random.rand()
    cur_total = 0
    for i in range(len(probs)):
        cur_total = cur_total+probs[i]
        if rad <= cur_total:
            return i


class DataGenerator(object):
    def __init__(self,
                 coord,
                 max_queue_size=1024*8,
                 wait_time=0.01):
        # Change the shape of the input data here with the parameter shapes.
        self.batch_size = 4
        self.wait_time = wait_time
        self.max_queue_size = max_queue_size
        self.queue = tf.RandomShuffleQueue(max_queue_size, min_after_dequeue= 8, dtypes=[tf.float32, tf.float32, tf.int32], shapes=[[N, N, numInputChannels], [N*N + 1], []])
        self.queue_size = self.queue.size()
        self.threads = []
        self.coord = coord
        self.sample_placeholder = [tf.placeholder(tf.float32, shape=[N, N, numInputChannels]), tf.placeholder(tf.float32, shape=[N*N + 1]), tf.placeholder(tf.int32, shape=[])]
        self.enqueue = self.queue.enqueue(self.sample_placeholder)

        self.board_input = tf.placeholder(tf.float32, shape=(self.batch_size, N, N, numInputChannels))
        self.gen_phase = tf.placeholder(tf.bool)
        self.nn_output = policy_value_net(self.board_input, numInputChannels, k, self.gen_phase)

    def dequeue(self, num_elements):
        output = self.queue.dequeue_many(num_elements)
        return output

    def generate_game_data(self, sess):           
        # x: input, y: next move probs, z: result of game
        #results = []

   

        # init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer(), name="init_node")    
 
        # sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))    
        # sess.run(init_op)

        # self.board_input = tf.placeholder(tf.float32, shape=(self.batch_size, N, N, numInputChannels))
        # self.nn_output = policy_value_net(self.board_input, numInputChannels, k, tf.placeholder(tf.bool))

        # load variables from tensorflow chkpt file

        completedQ = []

        root_nodes = []
        for i in range(self.batch_size):
            root_nodes.append(TreeNode(pos=empty_position()))
         #   results.append([])
            completedQ.append(False)


        #mcts_start_time = timeit.default_timer()
        #nn_time = 0

        while False in completedQ:
            # if root_node[0].pos.n % 2 == 1:
            #   player to move:

            #   input_data = sys.stdin.readline()

                # PLAYER MOVEs HERE: root_node[0].pos.move(c)
                # continue


            sim_nodes = []        
            input_batch = numpy.zeros((self.batch_size, N, N, numInputChannels))

            for ind in range(self.batch_size):
                cur_sim_nodes = tree_descend(root_nodes[ind])
                input_batch[ind] = process_input(cur_sim_nodes[-1].pos.board).astype(float)
                sim_nodes.append(cur_sim_nodes)

            # nn_start_time = timeit.default_timer()

            p, v = sess.run(self.nn_output, feed_dict={self.board_input: input_batch, self.gen_phase: 0})
            
            # nn_end_time = timeit.default_timer()
            # nn_time = nn_time + (nn_end_time - nn_start_time)

            for ind in range(self.batch_size):
                expand_node(sim_nodes[ind][-1], p[ind])
                tree_update(sim_nodes[ind], v[ind])
                if (root_nodes[ind].v < 100):
                    continue
                else:
                    cur_policy = search_policy(root_nodes[ind], temp=1)         

                    a = weight_sample(cur_policy)
                    c = numpy_ind_to_gs_ind(a)      # move selected by computer

                    # computer moves HERE
                    # output c to server 

                    #print(divmod(a, N))
                    # find child of root_node chosen
                    for c_node in root_nodes[ind].children:
                        if c_node.pos.last == c:
                            child_node = c_node
                            break

                    #root_input = process_input(root_nodes[ind].pos.board).astype(float)
                    if not completedQ[ind]:
                        #results[ind].append((root_input, cur_policy, -2 * (child_node.pos.n % 2) + 1))

                    if child_node.pos.n <= MAX_GAME_LEN and child_node.pos.pass_count < 3:
                        # continue playing
                        root_nodes[ind] = child_node
                        #print(ind)
                        #print(str_coord(child_node.pos.last))


                    else:
                        # indicate game has ended
                        completedQ[ind] = True

                        #print(completedQ)

                        final_score = child_node.pos.score()
                        
                        if ((child_node.pos.n % 2 == 0) and (final_score > 0)) or ((child_node.pos.n % 2 == 1) and (final_score < 0)):
                            value = 1
                        else:
                            value = -1

                        if not completedQ[ind]:
                            #for r in results[ind]:
                            #    r[2] = r[2] * value
        
        #mcts_end_time = timeit.default_timer()

        #print(('MCTS took %.2fs') % (mcts_end_time - mcts_start_time))
        #print(('Neural network took %.2fs') % (nn_time))

        #for ind in range(self.batch_size):
        #    for r in results[ind]:
        #        yield r[0], r[1], r[2] * value


    def thread_main(self, sess):
        stop = False
        while not stop:
            iterator = self.generate_game_data(sess)

            for data in iterator:
                while self.queue_size.eval(session=sess) == self.max_queue_size:
                    if self.coord.should_stop():
                        break
                    time.sleep(self.wait_time)
                if self.coord.should_stop():
                    stop = True
                    print("Enqueue thread receives stop request.")
                    break
                sess.run(self.enqueue, feed_dict={self.sample_placeholder[0]: data[0], 
                                                    self.sample_placeholder[1]: data[1], self.sample_placeholder[2]: data[2]})

    def start_threads(self, sess, n_threads=1):
        for _ in range(n_threads):
            thread = threading.Thread(target=self.thread_main, args=(sess,))
            thread.daemon = True  # Thread will close when parent quits.
            thread.start()
            self.threads.append(thread)
        return self.threads

    