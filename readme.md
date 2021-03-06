# Phrase Fill-in-blank Problem (PFP)　語句空欄補充問題

語句空欄補充問題 Phrase Fill-in-blank Problem (PFP)

## 希望要点
### ソースコードの条件

- ソースコードの仕様（特に出力メッセージ）をコメントで記入

- 再帰呼び出しや重要な関数（サブルーチン）は最初にプロトタイプ宣言されていること
例：int findMaxElem(int []);

### ソースコードからの空欄生成ルール

- 条件文：if文, while文の(　)の中
- 標準入出力文：printf文，scanf文の(　)の中
- 関数戻り値：return文の後　→main関数のreturn 0は除外
- if, while条件文の中に，対象の関数がある場合は，その関数の（　）の中のみ　**（変更あり）**
- 教員が指定する文全体（;を含む）→仕様の実現に重要な行の実装を学習
- 教員が指定する文では空欄を生成しない

## 実現した要点

### **注意点**

- **対象関数：main 関数以外の関数（現時点は0～1個のみ対応可能）**

- コードの同じ部分が，上のルールを既に満足した場合，下のルールは無視する．

  例：if文の()の中に対象関数がある，空欄になるのはその対象関数の（）の中のみ

- 結果のスペースとタブは消去される．

### 実現したルール（順番に）

- [x] 指定した空欄に**しない**部分
  - [x] 行のはじめから，`[noblankbefore]`まで
  - [x] `[noblankbetween]`から，`[/noblankbetween]`まで
- [x] 指定した空欄に**する**部分
  - [x] 行のはじめから，`[blankbefore]`まで
  - [x] `[blankbetween]`から，`[/blankbetween]`まで
- [x] 対象関数の（）の中
- [x] 条件文：if文, while文の(　)の中
- [x] 標準入出力文：printf文，scanf文の(　)の中
- [x] 関数戻り値：return文の後(main関数のreturn 0は除外)
- [x] キャスト（型変換）（num = (int)chrなど）

## 使い方

usage: `python process.py [-h] source_dir`

```
Creating blanks for C language source code files

positional arguments:
  source_dir  The directory containing source code files to be processed.

optional arguments:
  -h, --help  show this help message and exit
```
