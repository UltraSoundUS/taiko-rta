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

10,000良 カテゴリで、曲と曲のインターバルを 30 秒と見積もったときのルートを求める。

```bash
python src/solve.py -c 10000 -i 30 csv/most_difficult_songs.csv
```

以下のように出力される。

```log
[Oct 26 20:18:14] INFO     Song list: {'第六天魔王(裏譜面)': 3, 'Infinite
                           Rebellion': 3, '第六天魔王': 1}
                  INFO     Total time: 1045.7
                  INFO     Total combo: 10054
```

10,000良 (no duplicate) カテゴリで、曲と曲のインターバルを 30 秒と見積もったときのルートを求める。

```bash
python src/solve.py -c 10000 -i 30 -nd csv/most_difficult_songs.csv
```

以下のように出力される。

```log
[Oct 27 02:30:14] INFO     Song list: {'第六天魔王(裏譜面)': 1, 'Infinite
                           Rebellion': 1, '幽玄ノ乱': 1, 'Central Dogma
                           Pt.1(裏譜面)': 1, '赤と白薔薇の魔女': 1,
                           'ダンガンノーツ(裏譜面)': 1,
                           '憎悪と醜悪の花束(裏譜面)': 1, 'Calamity
                           Fortune(裏譜面)': 1}
                  INFO     Total time: 1185.4
                  INFO     Total combo: 10072
```
