import os
import sys
import timeit
import pickle

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import math

def draw_board(input, stone_color):

   fig = plt.figure(figsize = [19,19])
   fig.patch.set_facecolor((1, 1, 0.8))
   ax = fig.add_subplot(111)
   
   full_size = int(math.sqrt(len(input)))
   board_size = full_size-2

   board = np.array([s for s in input]).reshape(full_size, full_size)[1:-1,1:-1]

   # draw the grid
   for x in range(board_size):
      ax.plot([x, x], [0, board_size-1], 'k')
   for y in range(board_size):
      ax.plot([0, board_size-1], [y, y], 'k')
   
   # scale the axis area to fill the whole figure
   ax.set_position([0, 0, 1, 1])
   
   # get rid of axes and everything (the figure background will show through)
   ax.set_axis_off()
   
   # scale the plot area conveniently (the board is in 0,0..18,18)
   ax.set_xlim(-1, board_size)
   ax.set_ylim(-1, board_size)
   
   if stone_color is not None:
       facecolor = {'X':'#000000', 'x':'#ffffff'} if stone_color=='Black' else {'X':'#ffffff', 'x':'#000000'}
       for i in range(board_size):        
           for j in range(board_size):
               if board[i,j] in ['X','x']:
                   ax.plot(j, board_size - i - 1, 'o',
                       markersize = 210.0/board_size,
                       markeredgecolor = 'k',
                       markerfacecolor = facecolor[board[i,j]],
                       markeredgewidth = 1)
               if board[i,j] == 'M':
                   ax.plot(j, board_size - i - 1, 'o',
                       markersize = 300.0/board_size,
                       markeredgecolor = 'r',
                       markerfacecolor = facecolor['X'],
                       markeredgewidth = 1)
                   ax.text(0, board_size-0.5, 
                       stone_color+': ({0},{1})'.format(j, board_size-i-1),
                       fontsize=20, horizontalalignment='left', color='b')
               if board[i,j] == '#':
                   ax.plot(j, board_size - i - 1, 'o',
                       markersize = 210.0/board_size,
                       markeredgecolor = 'k',
                       markerfacecolor = facecolor['x'],
                       markeredgewidth = 1)
                   ax.plot(j, board_size - i - 1, 'x',
                       markersize = 210.0/board_size,
                       markeredgecolor = 'g',
                       markeredgewidth = 1)
               if board[i,j] == 'K':
                   ax.plot(j, board_size - i - 1, 'o',
                       markersize = 210.0/board_size,
                       markeredgecolor = 'k',
                       markerfacecolor = facecolor['x'],
                       markeredgewidth = 1)
                   ax.plot(j, board_size - i - 1, 'x',
                       markersize = 210.0/board_size,
                       markeredgecolor = 'r',
                       markeredgewidth = 1)
        
   return ax  

def draw_board_old(input):
   # takes in numpy array of floats as input
   board_size = int(math.sqrt(input.size))

   fig = plt.figure(figsize = [8,8])
   fig.patch.set_facecolor((1, 1, 0.8))
   
   ax = fig.add_subplot(111)
   
   # draw the grid
   for x in range(board_size):
      ax.plot([x, x], [0, board_size-1], 'k')
   for y in range(board_size):
      ax.plot([0, board_size-1], [y, y], 'k')
   
   # scale the axis area to fill the whole figure
   ax.set_position([0, 0, 1, 1])
   
   # get rid of axes and everything (the figure background will show through)
   ax.set_axis_off()
   
   # scale the plot area conveniently (the board is in 0,0..18,18)
   ax.set_xlim(-1, board_size)
   ax.set_ylim(-1, board_size)
   
   #ax.plot(actualMove // 19, 18 - (actualMove % 19), 'o', markersize=28, markerfacecolor='r', markeredgewidth=1)
   
   for r in range(board_size):      
      for c in range(board_size):
            ind = r * board_size + c
            
            if input[ind] == 1.0:
                  ax.plot(c, board_size - r - 1, 'o',
                     markersize = 420.0/board_size,
                     markeredgecolor = 'k',
                     markerfacecolor = '#000000',
                     markeredgewidth = 1)
            elif input[ind] == -1.0:
                  ax.plot(c, board_size - r - 1, 'o',
                     markersize = 420.0/board_size,
                     markeredgecolor = 'k',
                     markerfacecolor = '#ffffff',
                     markeredgewidth = 1)
   
   plt.show()



