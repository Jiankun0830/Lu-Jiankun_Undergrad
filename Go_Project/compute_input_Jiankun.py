import sys, json, numpy
import time

import tensorflow as tf
import operator
import math
import timeit
import threading

from game_state import board_state_to_numpy_arr, process_input, empty_position
from tf_neural_net import policy_value_net


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


def tree_descend(root_node, disp=False):
    """ Descend through the tree to a leaf """
    root_node.v += 1
    nodes_list = [root_node]
    passes = 0

    cur_node = root_node

    while cur_node.children is not None and passes < 2:
        # if disp:
        #  print_pos(cur_node.pos)

        # Pick the most urgent child
        children = list(cur_node.children)

        # if disp:
        #   for c in children:
        #     dump_subtree(c, recurse=False)

        cur_node = max(children, key=lambda c: (float(c.w) / (1 + c.v)) + c.pb * math.sqrt(
            5.0 * math.log(1 + cur_node.v) / (1 + c.v)))

        nodes_list.append(cur_node)

        # if disp:
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
        # if disp:
        #  print('updating', str_coord(node.pos.last), score < 0, file=sys.stderr)

        node.w += score < 0  # score is for to-play, node statistics for just-played

        if node.children is not None:
            for child in node.children:
                if child.pos.last is None:
                    continue

        score = -score


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


def search_policy(node, temp=1):
    output = numpy.zeros(N * N + 1)

    for c in node.children:
        # print(c.pos.last)
        # print(c.v)
        ind = gs_ind_to_numpy_ind(c.pos.last)

        output[ind] = c.v ** (1 / temp)

    return output / numpy.sum(output)


def weight_sample(probs):
    rad = numpy.random.rand()
    cur_total = 0
    for i in range(len(probs)):
        cur_total = cur_total + probs[i]
        if rad <= cur_total:
            return i


def numpy_ind_to_gs_ind(ind):
    if ind == N * N:
        return None
    else:
        row = ind // N
        col = ind % N
        return W + 1 + (row * W) + col


N = 7
W = N + 2
numInputChannels = 2
k = 32
MAX_GAME_LEN = N * N * 2

batch_size = 1


def main():
    # get our data as an array from read_in()
    continue_reading = True

    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer(), name="init_node")

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
    sess.run(init_op)

    board_input = tf.placeholder(tf.float32, shape=(batch_size, N, N, numInputChannels))
    nn_output = policy_value_net(board_input, numInputChannels, k, tf.placeholder(tf.bool))
    gen_phase = tf.placeholder(tf.bool)

    completedQ = []
    root_nodes = []

    for i in range(batch_size):
        root_nodes.append(TreeNode(pos=empty_position()))
        #   results.append([])
        completedQ.append(False)

    while continue_reading:
        input_data = sys.stdin.readline()

        if input_data == 'End':
            continue_reading = False
            print("Finished!")
            continue

        if root_nodes[0].pos.n % 2 == 1:
            parsed = json.loads(input_data)
            i = parsed['i']
            j = parsed['j']
            c = i + (N + 2) * j + N + 3

            #   player to move:
            root_nodes[0].pos.move(c)
            continue

        sim_nodes = []
        input_batch = numpy.zeros((batch_size, N, N, numInputChannels))

        for ind in range(batch_size):
            cur_sim_nodes = tree_descend(root_nodes[ind])
            input_batch[ind] = process_input(cur_sim_nodes[-1].pos.board).astype(float)
            sim_nodes.append(cur_sim_nodes)

        # nn_start_time = timeit.default_timer()

        p, v = sess.run(nn_output, feed_dict={board_input: input_batch, gen_phase: 0})

        # nn_end_time = timeit.default_timer()
        # nn_time = nn_time + (nn_end_time - nn_start_time)

        for ind in range(batch_size):
            expand_node(sim_nodes[ind][-1], p[ind])
            tree_update(sim_nodes[ind], v[ind])
            if (root_nodes[ind].v < 100):
                continue
            else:
                cur_policy = search_policy(root_nodes[ind], temp=1)

                a = weight_sample(cur_policy)
                c = numpy_ind_to_gs_ind(a)  # move selected by computer
                j = int((c - N - 3) / (N + 2))
                i = c - N - 3 - (N + 2) * j
                output = {'j': j, 'i': i}
                print(json.dumps(output))
                sys.stdout.flush()

                # computer moves HERE
                # output c to server

                # print(divmod(a, N))
                # find child of root_node chosen
                for c_node in root_nodes[ind].children:
                    if c_node.pos.last == c:
                        child_node = c_node
                        break

                # root_input = process_input(root_nodes[ind].pos.board).astype(float)
                # if not completedQ[ind]:
                # results[ind].append((root_input, cur_policy, -2 * (child_node.pos.n % 2) + 1))

                if child_node.pos.n <= MAX_GAME_LEN and child_node.pos.pass_count < 3:
                    # continue playing
                    root_nodes[ind] = child_node
                    # print(ind)
                    # print(str_coord(child_node.pos.last))


                else:
                    # indicate game has ended
                    completedQ[ind] = True

                    # print(completedQ)

                    final_score = child_node.pos.score()

                    if ((child_node.pos.n % 2 == 0) and (final_score > 0)) or (
                                (child_node.pos.n % 2 == 1) and (final_score < 0)):
                        value = 1
                    else:
                        value = -1

                    if not completedQ[ind]:
                # for r in results[ind]:
                #    r[2] = r[2] * value

                # mcts_start_time = timeit.default_timer()
                # nn_time = 0


# start process
if __name__ == '__main__':
    main()