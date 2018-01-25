import sys, json, numpy
import time

import tensorflow as tf
import operator
import math
import timeit
import threading

from game_state import empty_position

myboard = empty_position()
print (myboard.board)