# ==============================================================================
# Original File: connectcsv.py
# Copyright (C) abpaudel (https://github.com/abpaudel/8-puzzle)
#
# This file is part of "8-puzzle" and is licensed under the
# GNU General Public License v3.0 (GPLv3).
# See <https://www.gnu.org/licenses/gpl-3.0.en.html> for details.
# ==============================================================================
# Modifications
# 2026-06-09: Igakg (15-puzzle適応)
#   - [変更内容1: 空ファイルをスキップする処理を追加]
# 2026-06-10: Igakg
#   - [変更内容2: globの結果からoutput_{method}_combined.csv自身を除外し、再実行時の自己参照を防止]
# ==============================================================================
from sys import argv
import glob

def connectcsv():
    method = argv[1]
    combined_name = f'output_{method}_combined.csv'
    files = [f for f in glob.glob(f'output_{method}*.csv') if f != combined_name]

    with open(combined_name, 'w') as outfile:
        outfile.write('cost_of_path,nodes_expanded,nodes_explored,search_depth,max_search_depth\n')
        for fname in files:
            with open(fname) as infile:
                header = infile.readline()
                if not header:
                    continue  # 空ファイルならスキップ
                for line in infile:
                    outfile.write(line)
            outfile.write('\n')

if __name__ == "__main__":
    connectcsv()