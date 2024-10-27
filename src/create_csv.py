"""FireFox からコピーしたテキストデータを CSV ファイルに変換するスクリプト。

Copyright (c) 2024 UltraSoundUS. All rights reserved.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd


def create_data(text: str) -> pd.DataFrame:
    """テキストデータからデータフレームを作成する。

    Args:
        text (str): テキストデータ。

    Returns:
        pd.DataFrame: データフレーム。
    """
    # テキストデータを行ごとに分割する。
    # 行の手前に空白がある場合は、空白を削除する。
    lines = [line.lstrip().split("\t") for line in text.split("\n") if line]
    # ヘッダとデータを取得する。
    header, data = lines[0], lines[1:]

    table = pd.DataFrame(data, columns=header)

    # 曲名、平均密度、音符数-1 の列のみを残す。
    return table[["曲名", "平均密度", "音符数-1"]]


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする。

    Returns:
        argparse.Namespace: パースした結果のオブジェクト。
    """
    parser = argparse.ArgumentParser(
        description="FireFox からコピーしたテキストデータを CSV ファイルに変換するスクリプト。"
    )
    parser.add_argument("text_file", type=Path, help="テキストファイル。")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力ファイル。",
    )

    return parser.parse_args()


def main() -> None:
    """メインの処理。"""
    args = parse_args()

    # テキストデータを読み込む。
    text = args.text_file.read_text(encoding="utf_8_sig")
    # データフレームを作成する。
    data = create_data(text)
    # CSV ファイルに書き込む。
    # args.output が指定されていない場合は、標準出力に書き込む。
    data.to_csv(args.output if args.output is not None else sys.stdout, index=False)


if __name__ == "__main__":
    main()
