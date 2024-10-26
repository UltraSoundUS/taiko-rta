# 太鼓の達人の RTA のルートを求める。

太鼓の達人の n 良の RTA のルートを求める。

## How to use

### Requirements

Windows で実行することを想定している。

- Python >= 3.10

### 必要パッケージをインストール

`pyproject.toml` に記載されているパッケージをインストールする。

```bash
pip install .
```

### SCIP をインストール

SCIP をインストールする。[SCIP 公式ページ](https://www.scipopt.org/index.php#download) からダウンロードしてインストールする。

インストール先から `scip.exe` を `bin/` ディレクトリにコピーする。

### データの準備

`csv/` ディレクトリ以下に曲のデータを CSV ファイルとして用意する。
形式は [`csv/most_difficult_songs.csv`](csv/most_difficult_songs.csv) を参照。

データは [太鼓の達人 譜面とか Wiki / 平均密度順/おに/★×10](https://wikiwiki.jp/taiko-fumen/%E5%8F%8E%E9%8C%B2%E6%9B%B2/%E5%B9%B3%E5%9D%87%E5%AF%86%E5%BA%A6%E9%A0%86/%E3%81%8A%E3%81%AB/%E2%98%85%C3%9710) 等を参考にしている。

### ルートを求める

良 10,000 カテゴリで、曲と曲のインターバルを 30 秒と見積もったときのルートを求める。

```bash
python src/solve.py -c 10000 -i 30 csv/most_difficult_songs.csv
```

以下のように出力される。

```log
[Oct 26 20:18:14] INFO     Song list: {'第六天魔王(裏譜面)': 3, 'Infinite Rebellion': 2, '第六天魔王': 1}      solve.py:76
                  INFO     Total time: 1045.7                                                                  solve.py:77
                  INFO     Total combo: 10054                                                                  solve.py:78
```
