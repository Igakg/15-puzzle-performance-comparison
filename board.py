# ==============================================================================
# Original File: board.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the 
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-08: Igakg
#   - [変更内容1: ゴール状態を1,2,3,4,5,6,7,8,0から1,2,3,8,0,4,7,6,5に変更し、GOAL定数として定義]
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容2: GOALを[1,2,...,15,0](4x4)に変更]
#   - [変更内容3: find_0のrange(9)→range(16)に変更]
#   - [変更内容4: __str__を4行表示に変更]
#   - [変更内容5: manhattan/indexの計算をグリッド幅4に変更(//3→//4, %3→%4, range(9)→range(16))]
#   - [変更内容6: up/down/left/rightの境界判定をグリッド幅4に変更]
# ==============================================================================

import numpy as np

GOAL = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])


class Board:
    parent = None
    state = None
    operator = None
    depth = 0
    zero = None
    cost = 0

    def __init__(self, state, parent=None, operator=None, depth=0):
        self.parent = parent
        self.state = np.array(state)
        self.operator = operator
        self.depth = depth
        self.zero = self.find_0()
        self.cost = self.depth + self.manhattan()

    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            op_pr = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
            return op_pr[self.operator] < op_pr[other.operator]

    def __str__(self):
        return str(self.state[:4]) + '\n' \
               + str(self.state[4:8]) + '\n' \
               + str(self.state[8:12]) + '\n' \
               + str(self.state[12:]) + ' ' + str(self.depth) + str(self.operator) + '\n'

    def goal_test(self):
        if np.array_equal(self.state, GOAL):
            return True
        else:
            return False

    def find_0(self):
        for i in range(16):
            if self.state[i] == 0:
                return i

    def manhattan(self):
        state = self.index(self.state)
        goal = self.index(GOAL)
        return sum((abs(state // 4 - goal // 4) + abs(state % 4 - goal % 4))[1:])

    @staticmethod
    def index(state):
        index = np.array(range(16))
        for x, y in enumerate(state):
            index[y] = x
        return index

    def swap(self, i, j):
        new_state = np.array(self.state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def up(self):
        if self.zero > 3:
            return Board(self.swap(self.zero, self.zero - 4), self, 'Up', self.depth + 1)
        else:
            return None

    def down(self):
        if self.zero < 12:
            return Board(self.swap(self.zero, self.zero + 4), self, 'Down', self.depth + 1)
        else:
            return None

    def left(self):
        if self.zero % 4 != 0:
            return Board(self.swap(self.zero, self.zero - 1), self, 'Left', self.depth + 1)
        else:
            return None

    def right(self):
        if (self.zero + 1) % 4 != 0:
            return Board(self.swap(self.zero, self.zero + 1), self, 'Right', self.depth + 1)
        else:
            return None

    def neighbors(self):
        neighbors = [self.up(), self.down(), self.left(), self.right()]
        return list(filter(None, neighbors))

    __repr__ = __str__