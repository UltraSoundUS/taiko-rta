"""太鼓の達人の RTA のルートを求めるプログラム。

Copyright (c) 2024 UltraSoundUS. All rights reserved.
"""

import argparse
import json
import sys
from logging import INFO, WARNING, basicConfig, getLogger
from pathlib import Path

import pandas as pd
import pulp
from rich.logging import RichHandler


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする。

    Returns:
        argparse.Namespace: パースした結果のオブジェクト。
    """
    parser = argparse.ArgumentParser(description="太鼓の達人の RTA のルートを求めるプログラム。")
    parser.add_argument("csv_file", type=Path, help="曲の情報が記載された CSV ファイル。")
    parser.add_argument(
        "-c", "--combo", type=int, default=20_000, help="RTA レギュレーションに必要なコンボ数。"
    )
    parser.add_argument("-i", "--interval", type=int, default=20, help="曲と曲とのインターバル。")
    parser.add_argument("-o", "--output", type=Path, help="結果を出力するファイル。")
    parser.add_argument("-v", "--verbose", action="store_true", help="詳細な情報を表示する。")
    parser.add_argument(
        "-nd", "--no-duplicate", action="store_true", help="同じ曲を複数回演奏しない。"
    )

    return parser.parse_args()


def main() -> None:
    """メインの処理。"""
    args = parse_args()

    # ログを設定する。
    logger = getLogger(__name__)
    basicConfig(
        level=INFO if args.verbose else WARNING,
        format="%(message)s",
        datefmt="[%b %d %X]",
        handlers=[RichHandler()],
    )

    # ソルバーに FSCIP を指定。
    # bin/ ディレクトリに scip.exe を設置する。
    solver = pulp.SCIP_CMD("bin/scip.exe", msg=False)

    # CSV からデータを読み込む。
    data = pd.read_csv(args.csv_file, comment="#")

    # 演奏時間を計算する。
    data["演奏時間"] = data["音符数-1"] / data["平均密度"]
    # コンボ数を計算する。
    data["コンボ数"] = data["音符数-1"] + 1

    # 必要なコンボ数。
    required_combo = args.combo
    # 曲と曲の間のインターバル。
    interval_between_songs = args.interval

    # モデルを作成する。
    model = pulp.LpProblem("Optimize_RTA_route", pulp.LpMinimize)
    # 変数を作成する。
    # 曲を何回演奏するかを表す変数。
    # 0 以上の整数値。
    x = (
        pulp.LpVariable.dicts("x", data.index, lowBound=0, upBound=1, cat=pulp.LpInteger)
        if args.no_duplicate
        else pulp.LpVariable.dicts("x", data.index, lowBound=0, cat=pulp.LpInteger)
    )

    # 曲を演奏している時間を最小化する。
    playing_time = pulp.lpSum(data["演奏時間"][i] * x[i] for i in data.index)
    # 曲と曲の間のインターバルは、曲数 - 1 だけかかる。
    playing_time += interval_between_songs * (pulp.lpSum(x[i] for i in data.index) - 1)
    # 目的関数を設定する。
    model += playing_time

    # 制約条件を設定する。
    # コンボ数が必要な数以上になるようにする。
    model += pulp.lpSum(data["コンボ数"][i] * x[i] for i in data.index) >= required_combo

    # モデルを解く。
    model.solve(solver)
    if pulp.LpStatus[model.status] != "Optimal":
        logger.warning("No optimal solution was found.")

    # 変数の値を表示する。
    info = {data["曲名"][i]: int(round(x[i].value())) for i in data.index if x[i].value() > 0}
    logger.info(f"Status: {pulp.LpStatus[model.status]}")  # noqa: G004
    logger.info(f"Number of songs: {len(info)}")  # noqa: G004
    logger.info(f"Total time: {model.objective.value():.1f}")  # noqa: G004
    logger.info(f"Total combo: {sum(data['コンボ数'][i] * x[i].value() for i in data.index):.0f}")  # noqa: G004
    logger.info(f"Song list: {info}")  # noqa: G004

    # 結果をファイルに出力する。
    if args.output is None:
        json.dump(info, sys.stdout, indent=4, ensure_ascii=False)
    else:
        with args.output.open("w", encoding="utf_8") as f:
            json.dump(info, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
