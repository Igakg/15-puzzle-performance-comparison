# 15-puzzle-performance-comparison

15パズルを複数の探索アルゴリズムで解き、そのパフォーマンスを比較するツールです。  
IDS・A*(h0)・A*(h1)・A*(h2) の4アルゴリズムを対象に、ランダム初期状態で実行し、CSVに結果を出力します。  
`MAX_NODES`（デフォルト: 5,000,000）を超えた探索は強制終了し、結果を `-1` として記録します。

> **原作**: [abpaudel/8-puzzle](https://github.com/abpaudel/8-puzzle) (GPLv3)  
> **改変**: Igakg（2026年）

[English README](README.md)

---

## アルゴリズム

| 識別子 | アルゴリズム | ヒューリスティック |
| ------ | ------------ | ------------------ |
| `ids` | Iterative Deepening Search (IDS) | なし |
| `ast0` | A* | h(n) = 0（ダイクストラ法と等価） |
| `ast1` | A* | h(n) = ミスプレース数（ゴールと異なる位置にあるタイル数） |
| `ast2` | A* | h(n) = マンハッタン距離（各タイルのゴールまでの距離の総和） |

**ゴール状態**:

```text
 1  2  3  4
 5  6  7  8
 9 10 11 12
13 14 15  0
```

---

## 探索ノード数の上限

非効率なアルゴリズムが無限に実行されるのを防ぐため、探索済みノード数が `MAX_NODES` に達した時点で全ソルバーを強制終了します。  
上限値は `solver.py` で定義されています：

```python
MAX_NODES = 5_000_000
```

上限を超えた場合、出力CSVの `nodes_explored` 以外のカラムはすべて `-1` となります。

> **IDSの `nodes_explored` について**: IDSは深さイテレーションのたびに探索済みセットをリセットするため、`nodes_explored` は**全イテレーションの累積合計**を報告します。上限チェックはイテレーション終了後に行われるため（途中ではなく）、最後のイテレーションで探索したノード数の分だけ `MAX_NODES` を超えた値になることがあります。

---

## セットアップ

### 必要環境

- Python 3.x
- numpy

### インストール

```bash
git clone <リポジトリURL>
cd 15-puzzle-performance-comparison
python3 -m venv venv
source venv/bin/activate
pip install numpy
```

---

## 使い方

### 特定の初期状態で実行

```bash
python main.py <アルゴリズム> <初期状態>
```

例：

```bash
python main.py ast2 "[1,2,3,4,5,6,7,8,9,10,11,12,13,0,14,15]"
```

### ランダム初期状態で実行

```bash
python main.py <アルゴリズム> random [n]
```

`n` で実行回数を指定します（省略時はデフォルト5回）。

例：

```bash
python main.py ids random          # 5回（デフォルト）
python main.py ast0 random 100     # 100回
python main.py ast1 random 50
python main.py ast2 random 100
```

`random` モードでは解ける状態のみを生成し、各実行結果を個別CSVに出力します。

---

## 出力ファイル

実行後、以下の形式でCSVが生成されます：

```text
output_<アルゴリズム>_<連番>.csv
```

各CSVの内容：

| カラム | 説明 |
| ------ | ---- |
| `cost_of_path` | 解までの手数（上限超過時は `-1`） |
| `nodes_expanded` | 展開ノード数（上限超過時は `-1`） |
| `nodes_explored` | 探索済みノード数 |
| `search_depth` | 解の深さ（上限超過時は `-1`） |
| `max_search_depth` | 最大到達深さ（上限超過時は `-1`） |

### CSVを1ファイルにまとめる

```bash
python connectcsv.py <アルゴリズム>
```

例：

```bash
python connectcsv.py ast2
```

`output_ast2_combined.csv` が生成されます。

---

## ファイル構成

```text
15-puzzle-performance-comparison/
├── main.py          # エントリーポイント・ランダム状態生成
├── board.py         # ボード状態・移動・ヒューリスティック定義（4x4）
├── solver.py        # 抽象ソルバー基底クラス・MAX_NODES定数
├── ids.py           # IDS実装
├── astar0.py        # A*(h=0) 実装
├── astar1.py        # A*(ミスプレース数) 実装
├── astar2.py        # A*(マンハッタン距離) 実装
└── connectcsv.py    # 複数CSVの結合ツール
```

---

## ライセンス

このプロジェクトは [GNU General Public License v3.0](LICENSE) のもとで公開されています。  
原作者: [abpaudel](https://github.com/abpaudel/8-puzzle)
