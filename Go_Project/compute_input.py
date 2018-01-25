import sys, json, numpy as np
import time
import random


from game_state import empty_position,weight_sample

N = 7



def main():
    # get our data as an array from read_in()
    Playing = True
    myboard = empty_position()

    while Playing:

        input_data = sys.stdin.readline()

        parsed = json.loads(input_data)
        i = parsed['i']
        j = parsed['j']
        if i == -2:
            final_score = myboard.score()
            stone_color = 'Black' if myboard.n % 2 == 0 else 'White'

            if myboard.n % 2 == 0:
                if final_score > 0:
                    result = 'Black wins White %f'%abs(final_score)
                else:
                    result = 'White wins Black %f'%abs(final_score)
            else:
                if final_score > 0:
                    result = 'Black wins White %f'%abs(final_score)
                else:
                    result = 'White wins Black %f'%abs(final_score)

            output = {"Result": "%s" % result}
            print(json.dumps(output))
            sys.stdout.flush()
            break


        if i == -1:
            myboard.pass_move()
        else:
            c = i + (N + 2) * j + N + 3
            myboard = myboard.move(c)

        actions = []  # all possible moves
        probs = []  # probability vector
        for i in myboard.moves(0):
            actions.append(i)

        if (len(actions) == 0):
            myboard = myboard.pass_move()
            output = {'j': -1, 'i':-1 }
            print(json.dumps(output))
            sys.stdout.flush()
            continue

        probs = np.random.rand(len(actions))  # randomly assigned
        probs = probs / np.sum(probs)

        while len(actions) > 0:
            action_index = weight_sample(probs)
            c = actions[action_index]
            newboard = myboard.move(c)

            if newboard is not None:
                myboard = newboard
                j = int((c - N - 3) / (N + 2))
                i = c - N - 3 - (N + 2) * j
                output = {'j': j, 'i': i}
                print(json.dumps(output))
                sys.stdout.flush()
                break

            del actions[action_index]
            probs = np.delete(probs, action_index)
            probs = probs / np.sum(probs)

            if newboard is None:
                myboard = myboard.pass_move()
                output = {'j': -1, 'i': -1}
                print(json.dumps(output))
                sys.stdout.flush()

            if False:
                Playing = False
                final_score = myboard.score()
                stone_color = 'Black' if myboard.n % 2 == 0 else 'White'

                if myboard.n % 2 == 0:
                    result = 'Black wins White {0}'.format(final_score) if final_score > 0 else 'White wins Black {0}'.format(final_score)
                else:
                    result = 'White wins Black {0}'.format(final_score) if final_score > 0 else 'Black wins White {0}'.format(final_score)

                output = {"Result": "%s" % result}
                print(json.dumps(output))
                sys.stdout.flush()






if __name__ == '__main__':
    main()
