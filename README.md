# 太鼓の達人の RTA のルートを求める

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

以下のように実行する。

詳細のオプションは `python src/solve.py --help` で確認できる。

#### 10,000良 カテゴリで、曲と曲のインターバルを 30 秒と見積もったときのルートを求める。

```bash
python src/solve.py -c 10000 -i 30 csv/level10.csv
```

以下のように出力される。

```json
{
    "第六天魔王(裏譜面)": 3,
    "Infinite Rebellion": 3,
    "第六天魔王": 1
}
```

仮に json ファイルで保存したい場合は、以下のようにする。

```bash
python src/solve.py -c 10000 -i 30 -o output.json csv/level10.csv
```

`output.json` に以下のように保存される。

```json
{"第六天魔王(裏譜面)": 3, "Infinite Rebellion": 3, "第六天魔王": 1}
```

#### 10,000良 (no duplicate) カテゴリで、曲と曲のインターバルを 30 秒と見積もったときのルートを求める。

```bash
python src/solve.py -c 10000 -i 30 -nd csv/level10.csv
```

以下のように出力される。

```json
{
    "第六天魔王(裏譜面)": 1,
    "Infinite Rebellion": 1,
    "幽玄ノ乱": 1,
    "第六天魔王": 1,
    "Central Dogma Pt.1(裏譜面)": 1,
    "モノクロボイス(裏譜面)": 1,
    "赤と白薔薇の魔女": 1,
    "冷凍庫CJ ～嗚呼面太鼓ブラザーズ～": 1
}
```
