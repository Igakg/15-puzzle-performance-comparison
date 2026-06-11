# ==============================================================================
# Original File: solver.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-02: Igakg
#   - [変更内容1: initにset()を追加、10回生成において、前の状態をリセットする]
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容2: MAX_NODES定数を追加(探索ノード数の上限)]
# 2026-06-10: Igakg
#   - [変更内容3: MAX_NODESのデフォルト値を1,000,000に変更]
# ==============================================================================

MAX_NODES = 1_000_000

from abc import ABC, abstractmethod


class Solver(ABC):
    solution = None
    frontier = None
    nodes_expanded = 0
    max_depth = 0
    explored_nodes = set()
    initial_state = None

    def __init__(self, initial_state):
        self.explored_nodes = set()
        self.initial_state = initial_state

    def ancestral_chain(self):
        current = self.solution
        chain = [current]
        while current.parent is not None:
            chain.append(current.parent)
            current = current.parent
        return chain

    @property
    def path(self):
        path = [node.operator for node in self.ancestral_chain()[-2::-1]]
        return path

    @abstractmethod
    def solve(self):
        pass

    def set_solution(self, board):
        self.solution = board
        self.nodes_expanded = len(self.explored_nodes) - len(self.frontier) - 1
        # return self.solution