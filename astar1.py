# ==============================================================================
# Original File: astar1.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容1: ヒューリスティックをGOALと比較する正しい不一致タイル数に修正]
#   - [変更内容2: 探索ノード数がMAX_NODESを超えた場合にループを強制終了]
# ==============================================================================
import heapq
from board import GOAL
from solver import Solver, MAX_NODES

class AStar1(Solver):
    def __init__(self, initial_state):
        super(AStar1, self).__init__(initial_state)
        self.frontier = []

    @staticmethod
    def h(board):
        return sum(1 for i, v in enumerate(board.state) if v != 0 and v != GOAL[i])

    def solve(self):
        self.initial_state.cost = self.initial_state.depth + self.h(self.initial_state)
        heapq.heappush(self.frontier, self.initial_state)
        while self.frontier:
            if len(self.explored_nodes) >= MAX_NODES:
                break
            board = heapq.heappop(self.frontier)
            self.explored_nodes.add(tuple(board.state))
            if board.goal_test():
                self.set_solution(board)
                break
            for neighbor in board.neighbors():
                if tuple(neighbor.state) not in self.explored_nodes:
                    neighbor.cost = neighbor.depth + self.h(neighbor)
                    heapq.heappush(self.frontier, neighbor)
                    self.explored_nodes.add(tuple(neighbor.state))
                    self.max_depth = max(self.max_depth, neighbor.depth)
        return
