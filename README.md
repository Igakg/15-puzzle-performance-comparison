# 15-puzzle-performance-comparison

A tool to solve the 15-puzzle with multiple search algorithms and compare their performance.  
Runs IDS, A*(h0), A*(h1), and A*(h2) on random initial states, outputting results to CSV.  
Searches that exceed `MAX_NODES` (default: 100,000) are forcibly terminated and recorded as `-1`.

> **Original**: [abpaudel/8-puzzle](https://github.com/abpaudel/8-puzzle) (GPLv3)  
> **Modified by**: Igakg (2026)

[日本語版 README はこちら](README.ja.md)

---

## Algorithms

| Identifier | Algorithm | Heuristic |
|------------|-----------|-----------|
| `ids`  | Iterative Deepening Search (IDS) | None |
| `ast0` | A* | h(n) = 0 (equivalent to Dijkstra) |
| `ast1` | A* | h(n) = Number of misplaced tiles |
| `ast2` | A* | h(n) = Manhattan distance |

**Goal state**:
```
 1  2  3  4
 5  6  7  8
 9 10 11 12
13 14 15  0
```

---

## Node Limit

To prevent inefficient algorithms from running indefinitely, all solvers stop when the number of explored nodes reaches `MAX_NODES`.  
The limit is defined in `solver.py`:

```python
MAX_NODES = 100_000
```

When the limit is exceeded, the output CSV contains `-1` for all metrics except `nodes_explored`.

> **Note on IDS `nodes_explored`**: IDS resets its explored set at the start of each depth iteration, so `nodes_explored` reports the **cumulative total** across all iterations. Because the limit is checked after each full iteration completes (not mid-iteration), the reported value may exceed `MAX_NODES` by the number of nodes explored in the final iteration.

---

## Setup

### Requirements
- Python 3.x
- numpy

### Installation

```bash
git clone <repository-url>
cd 15-puzzle-performance-comparison
python3 -m venv venv
source venv/bin/activate
pip install numpy
```

---

## Usage

### Run with a specific initial state

```bash
python main.py <algorithm> <initial_state>
```

Example:
```bash
python main.py ast2 "[1,2,3,4,5,6,7,8,9,10,11,12,13,0,14,15]"
```

### Run with random initial states

```bash
python main.py <algorithm> random [n]
```

`n` specifies the number of runs (default: 5).

Example:
```bash
python main.py ids random        # runs 5 times (default)
python main.py ast0 random 100   # runs 100 times
python main.py ast1 random 50
python main.py ast2 random 100
```

In `random` mode, only solvable states are generated. Results are written to individual CSVs for each run.

---

## Output Files

Each run produces a CSV file:

```
output_<algorithm>_<index>.csv
```

Columns:

| Column | Description |
|--------|-------------|
| `cost_of_path` | Number of moves to reach the goal (`-1` if limit exceeded) |
| `nodes_expanded` | Number of nodes expanded (`-1` if limit exceeded) |
| `nodes_explored` | Number of nodes explored |
| `search_depth` | Depth of the solution (`-1` if limit exceeded) |
| `max_search_depth` | Maximum depth reached during search (`-1` if limit exceeded) |

### Combine CSVs into one file

```bash
python connectcsv.py <algorithm>
```

Example:
```bash
python connectcsv.py ast2
```

Produces `output_ast2_combined.csv`.

---

## File Structure

```
15-puzzle-performance-comparison/
├── main.py          # Entry point & random state generation
├── board.py         # Board state, moves, and heuristics (4x4)
├── solver.py        # Abstract solver base class & MAX_NODES constant
├── ids.py           # IDS implementation
├── astar0.py        # A*(h=0) implementation
├── astar1.py        # A*(misplaced tiles) implementation
├── astar2.py        # A*(Manhattan distance) implementation
└── connectcsv.py    # Tool to combine multiple CSVs
```

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).  
Original author: [abpaudel](https://github.com/abpaudel/8-puzzle)
