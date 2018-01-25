from __future__ import print_function
from collections import namedtuple
from itertools import count
import math
import random
import re
import sys
import time
import numpy as np

import matplotlib.pyplot as plt
from plot import draw_board

# Given a board of size NxN (N=9, 19, ...), we represent the position
# as an (N+1)*(N+2) string, with '.' (empty), 'X' (to-play player),
# 'x' (other player), and whitespace (off-board border to make rules
# implementation easier).  Coordinates are just indices in this string.
# You can simply print(board) when debugging.
N = 7
W = N + 2
empty = ''.join([(N + 2) * ' '] + N * [' ' + N * '.' + ' '] + [(N + 2) * ' '])
ax_empty = draw_board(empty, None)  # draw an empty board

colstr = 'ABCDEFGHJKLMNOPQRST'
MAX_GAME_LEN = N * N * 2


def neighbors(c):
    """ generator of coordinates for all neighbors of c """
    return [c - 1, c + 1, c - W, c + W]


def diag_neighbors(c):
    """ generator of coordinates for all diagonal neighbors of c """
    return [c - W - 1, c - W + 1, c + W - 1, c + W + 1]


def board_put(board, c, p):
    return board[:c] + p + board[c + 1:]


def floodfill(board, c):
    """ replace continuous-color area starting at c with special color # """
    # This is called so much that a bytearray is worthwhile...
    byteboard = bytearray(board, 'utf8')
    p = byteboard[c]
    byteboard[c] = ord('#')
    fringe = [c]
    while fringe:
        c = fringe.pop()
        for d in neighbors(c):
            if byteboard[d] == p:
                byteboard[d] = ord('#')
                fringe.append(d)
    return byteboard.decode('utf8')  # bug fixed; original returned str(byteboard), which was not formatted properly


# Regex that matches various kind of points adjecent to '#' (floodfilled) points
contact_res = dict()
for p in ['.', 'x', 'X']:
    rp = '\\.' if p == '.' else p
    contact_res_src = ['#' + rp,  # p at right
                       rp + '#',  # p at left
                       '#' + '.' * (W - 1) + rp,  # p below
                       rp + '.' * (W - 1) + '#']  # p above
    contact_res[p] = re.compile('|'.join(contact_res_src), flags=re.DOTALL)


def contact(board, p):
    """ test if point of color p is adjacent to color # anywhere
    on the board; use in conjunction with floodfill for reachability """
    m = contact_res[p].search(board)
    if not m:
        return None
    return m.start() if m.group(0)[0] == p else m.end() - 1


def is_eyeish(board, c):
    """ test if c is inside a single-color diamond and return the diamond
    color or None; this could be an eye, but also a false one """
    eyecolor = None
    for d in neighbors(c):
        if board[d].isspace():
            continue
        if board[d] == '.':
            return None
        if eyecolor is None:
            eyecolor = board[d]
            othercolor = eyecolor.swapcase()
        elif board[d] == othercolor:
            return None
    return eyecolor


def is_eye(board, c):
    """ test if c is an eye and return its color or None """
    eyecolor = is_eyeish(board, c)
    if eyecolor is None:
        return None

    # Eye-like shape, but it could be a falsified eye
    falsecolor = eyecolor.swapcase()
    false_count = 0
    at_edge = False
    for d in diag_neighbors(c):
        if board[d].isspace():
            at_edge = True
        elif board[d] == falsecolor:
            false_count += 1
    if at_edge:
        false_count += 1
    if false_count >= 2:
        return None

    return eyecolor


class Position(namedtuple('Position', 'board ax size cap n pass_count ko last last2 komi')):
    """ Implementation of simple Chinese Go rules;
    n is how many moves were played so far """

    def move(self, c):
        """ play as player X at the given coord c, return the new position """

        # Are we trying to play in enemy's eye?
        in_enemy_eye = is_eyeish(self.board, c) == 'x'

        # Test for ko
        if c == self.ko:
            return None

        board = board_put(self.board, c, 'X')

        # Test for captures, and track ko
        capX = self.cap[0]
        singlecaps = []
        capindexes = []  # store cap indexes
        for d in neighbors(c):
            if board[d] != 'x':
                continue
            # XXX: The following is an extremely naive and SLOW approach
            # at things - to do it properly, we should maintain some per-group
            # data structures tracking liberties.
            fboard = floodfill(board, d)  # get a board with the adjacent group replaced by '#'
            if contact(fboard, '.') is not None:
                continue  # some liberties left
            # no liberties left for this group, remove the stones!
            capcount = fboard.count('#')
            capindexes = capindexes + [m.start() for m in re.finditer('#', fboard)]
            if capcount == 1:
                singlecaps.append(d)
            capX += capcount
            board = fboard.replace('#', '.')  # capture the group

            #print(c)
            #print(fboard)

        # Set ko
        ko = singlecaps[0] if in_enemy_eye and len(singlecaps) == 1 else None
        # Test for suicide
        if contact(floodfill(board, c), '.') is None:
            return None

        # Draw the move

        stone_color = 'Black' if self.n % 2 == 0 else 'White'

        showboard = list(board)
        showboard[c] = 'M'  # where to move
        if ko is not None:
            showboard[ko] = 'K'  # ko
        if len(capindexes) > 0:
            for ind in capindexes:
                showboard[ind] = '#'  # caps
        ax = draw_board(''.join(showboard), stone_color)
        ax.text((self.size - 1) / 2, self.size - 0.5, 'Caps: {0} to {1}'.format(capX, self.cap[1]), fontsize=20,
                color='b')

        # Update the position and return
        return Position(board=board.swapcase(), ax=ax, size=self.size,
                        cap=(self.cap[1], capX),
                        n=self.n + 1,
                        pass_count = self.pass_count,
                        ko=ko,
                        last=c,
                        last2=self.last,
                        komi=self.komi)

    def pass_move(self):
        """ pass - i.e. return simply a flipped position """
        stone_color = 'Black' if self.n % 2 == 0 else 'White'
        ax = draw_board(self.board, stone_color)
        ax.text(0, self.size - 0.5, stone_color + ': Pass', fontsize=20, horizontalalignment='left', color='b')
        ax.text((self.size - 1) / 2, self.size - 0.5, 'Caps: {0} to {1}'.format(self.cap[0], self.cap[1]), fontsize=20,
                color='b')
        pass_times = self.pass_count
        if self.last == None:
            pass_times += 1
        else:
            pass_times = 1
        return Position(board=self.board.swapcase(), ax=ax, size=self.size,
                        cap=(self.cap[1], self.cap[0]),
                        n=self.n + 1,
                        pass_count = pass_times,
                        ko=None,
                        last=None,
                        last2=self.last,
                        komi=self.komi)

    def moves(self, i0):
        """ Generate a list of moves (includes false positives - suicide moves;
        does not include true-eye-filling moves), starting from a given board
        index (that can be used for randomization) """
        i = i0 - 1
        passes = 0
        while True:
            i = self.board.find('.', i + 1)
            if passes > 0 and (i == -1 or i >= i0):
                break  # we have looked through the whole board
            elif i == -1:
                passes += 1
                continue  # go back and start from the beginning
            # Test for to-play player's one-point eye
            if is_eye(self.board, i) == 'X':
                continue
            yield i

    def last_moves_neighbors(self):
        """ generate a randomly shuffled list of points including and
        surrounding the last two moves (but with the last move having
        priority) """
        clist = []
        for c in self.last, self.last2:
            if c is None:  continue
            dlist = [c] + list(neighbors(c) + diag_neighbors(c))
            random.shuffle(dlist)
            clist += [d for d in dlist if d not in clist]
        return clist

    def score(self, owner_map=None):
        """ compute score for to-play player; this assumes a final position
        with all dead stones captured; if owner_map is passed, it is assumed
        to be an array of statistics with average owner at the end of the game
        (+1 black, -1 white) """
        board = self.board
        i = 0
        while True:
            i = self.board.find('.', i + 1)
            if i == -1:
                break
            fboard = floodfill(board, i)
            # fboard is board with some continuous area of empty space replaced by #
            touches_X = contact(fboard, 'X') is not None
            touches_x = contact(fboard, 'x') is not None
            if touches_X and not touches_x:
                board = fboard.replace('#', 'X')
            elif touches_x and not touches_X:
                board = fboard.replace('#', 'x')
            else:
                board = fboard.replace('#', ':')  # seki, rare
                # now that area is replaced either by X, x or :
        komi = self.komi if self.n % 2 == 1 else -self.komi
        if owner_map is not None:
            for c in range(W * W):
                n = 1 if board[c] == 'X' else -1 if board[c] == 'x' else 0
                owner_map[c] += n * (1 if self.n % 2 == 0 else -1)
        return board.count('X') - board.count('x') + komi


def empty_position():
    """ Return an initial board position """
    return Position(board=empty, ax=ax_empty, size=N,
                    cap=(0, 0),
                    n=0,
                    pass_count = 0,
                    ko=None,
                    last=None,
                    last2=None,
                    komi=7.5)


def board_state_to_numpy_arr(input):
    output = np.zeros(N * N)

    board = input.split('\n')[1:-1]

    ind = 0

    for row in board:
        for p in row:
            if p == 'X':
                output[ind] = 1
            elif p == 'x':
                output[ind] = -1

            ind = ind + 1

    return output


def process_input(board):
    bline = board.replace('\n', '').replace(' ', '')

    b = np.array([ord(c) for c in bline])

    black = np.equal(b, 88).astype(int).reshape((N, N))
    white = np.equal(b, 120).astype(int).reshape((N, N))

    channels = np.stack((black, white), axis=-1)

    return channels


### sample from probability vector
def weight_sample(probs):
    rad = np.random.rand()
    cur_total = 0
    for i in range(len(probs)):
        cur_total = cur_total + probs[i]
        if rad <= cur_total:
            return i


if __name__ == "__main__":

    # Generate an empty board
    myboard = empty_position()
    plt.show()


    method = 'Random'  # 'Deterministic' or 'Random'

    while myboard.n <= MAX_GAME_LEN and myboard.pass_count < 3:
        actions = []  # all possible moves
        probs = []  # probability vector

        for i in myboard.moves(0):
            actions.append(i)

        if (len(actions) == 0):
            myboard = myboard.pass_move()
            #plt.show(myboard.ax)
            continue

        probs = np.random.rand(len(actions))  # randomly assigned
        probs = probs / np.sum(probs)

        if method == 'Deterministic':
            actions = np.array(actions)[np.argsort(-probs)]
            for c in actions:
                newboard = myboard.move(c)
                #print(c)
                if newboard is not None:
                    myboard = newboard
                    #plt.show(myboard.ax)
                    break
        elif method == 'Random':
            while len(actions) > 0:
                action_index = weight_sample(probs)
                c = actions[action_index]

                newboard = myboard.move(c)

                if newboard is not None:
                    myboard = newboard
                    #plt.show(myboard.ax)
                    break

                del actions[action_index]
                probs = np.delete(probs, action_index)
                probs = probs / np.sum(probs)

        if newboard is None:
            myboard = myboard.pass_move()
            plt.show()

    final_score = myboard.score()
    stone_color = 'Black' if myboard.n % 2 == 0 else 'White'
    ax = draw_board(myboard.board, stone_color)
    if myboard.n % 2 == 0:
        result = 'Black wins White {0}'.format(final_score) if final_score > 0 else 'White wins Black {0}'.format(
            -final_score)
    else:
        result = 'White wins Black {0}'.format(final_score) if final_score > 0 else 'Black wins White {0}'.format(
            -final_score)
    ax.text((myboard.size - 1) / 2, myboard.size - 0.5, result, fontsize=20, horizontalalignment='center', color='b')
    plt.show()
