# ==============================================================================
# Original File: iddfs.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容1: 累積探索ノード数がMAX_NODESを超えた場合にループを強制終了]
#   - [変更内容2: total_exploredをインスタンス変数として保存し、正しい累積ノード数を出力に反映]
# ==============================================================================
import itertools

from solver import Solver, MAX_NODES


class IDS(Solver):
    def __init__(self, initial_state):
        super(IDS, self).__init__(initial_state)
        self.frontier = []
        self.total_explored = 0

    def dls(self, limit):
        self.frontier.append(self.initial_state)
        while self.frontier:
            board = self.frontier.pop()
            self.explored_nodes.add(tuple(board.state))
            if board.goal_test():
                self.set_solution(board)
                return self.solution
            if board.depth < limit:
                for neighbor in board.neighbors()[::-1]:
                    if tuple(neighbor.state) not in self.explored_nodes:
                        self.frontier.append(neighbor)
                        self.explored_nodes.add(tuple(neighbor.state))
                        self.max_depth = max(self.max_depth, neighbor.depth)
        return None

    def solve(self):
        for i in itertools.count():
            self.frontier = []
            self.explored_nodes = set()
            self.max_depth = 0
            self.frontier.append(self.initial_state)
            sol = self.dls(i)
            self.total_explored += len(self.explored_nodes)
            if sol is not None or self.total_explored >= MAX_NODES:
                break
        return