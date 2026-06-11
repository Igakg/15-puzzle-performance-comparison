# ==============================================================================
# Original File: astar.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-02: Igakg
#   - [変更内容1: AstarクラスをAStar2クラスにリネーム]
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容2: 探索ノード数がMAX_NODESを超えた場合にループを強制終了]
# ==============================================================================
import heapq

from solver import Solver, MAX_NODES


class AStar2(Solver):
    def __init__(self, initial_state):
        super(AStar2, self).__init__(initial_state)
        self.frontier = []

    def solve(self):
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
                    heapq.heappush(self.frontier, neighbor)
                    self.explored_nodes.add(tuple(neighbor.state))
                    self.max_depth = max(self.max_depth, neighbor.depth)
        return