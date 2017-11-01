# @Author: chenyu
# @Date:   20_Oct_2017
# @Email:  yu.chen@pku.edu.cn
# @Filename: config.py
# @Last modified by:   chenyu
# @Last modified time: 21_Oct_2017

import multiprocessing
import names
import os
NUM_CPU = multiprocessing.cpu_count()

MODE = 1  # 1: pure self play  2: between AI
if NUM_CPU < 10:
    NUMPARALELL = 2
else:
    NUMPARALELL = 15

NUM_SIMULATIONS = 400
INFERENCE_BATCHSIZE = 256
GAMEPARALELL = 10
TEMPERATURE = 0.6
EXPLORATION = 0.2
SIZE = 225
L = 6
GAMELENGTH = 30

DISTANCE = 1  # 0 mean no mask

LEARNINGRATE = 0.001
VALUE_DECAY = 1
