# 📁🌳 wintree

このライブラリは Windows 標準コマンドである`tree`コマンドの機能の少なさから生まれました。
`wintree` は、指定したディレクトリの階層構造をツリー形式で表示する Python ライブラリです。コマンドラインから簡単に使用でき、絵文字による視覚的なツリー表示や除外対象のディレクトリ指定も可能です。
ツリー構造を JSON で出力することで GUI アプリケーションにも活用できます。

## 🚀 使い方

### 📚️ ライブラリとして使用

```py
import wintree

print(wintree.tree())
```

```bash
# sample output
📂 root: .
├── 📄 .gitignore
├── 📄 README.md
├── 📄 pyproject.toml
├── 📁 src/
│   ├── 📁 assets/
│   │   ├── 📄 icon.png
│   │   └── 📄 splash_android.png
│   └── 📄 main.py
└── 📁 storage/
    ├── 📁 data/
    └── 📁 temp/
```

引数の指定

```py
from wintree import tree

print(tree(root_dir="/path/to/project", use_emoji=True, ignore_dirs=[".git", "__pycache__"], filter_exts=[".py",".txt"]))
```

| 引数名      | 型        | 説明                                                                                      |
| ----------- | --------- | ----------------------------------------------------------------------------------------- |
| root_dir    | str       | ツリー表示を開始するルートディレクトリのパス。デフォルトはカレントディレクトリ "."。      |
| use_emoji   | bool      | ツリー表示に絵文字を使用するかどうか。True にするとフォルダーやファイルにアイコンを付加。 |
| ignore_dirs | List[str] | ツリー表示から除外するディレクトリ名のリスト（部分一致）。例：[".git", "node_modules"]。  |
| filter_ext  | List[str] | 検出したいファイルの拡張子。例：[".py", ".txt"]。                                         |

JSON 形式で取得 or 保存

```py
# 辞書データを取得
data = wintree.tree_to_dict(show_meta=True)

# JSONファイルで保存
wintree.tree_to_json(root_dir="path/to/project" ,save_path="path/to/project_tree.json")
```

ツリー形状ではなくルートからの相対パスや絶対パスを縦に列挙することもできます。

```py
import wintree

print(wintree.list_files())
```

### ⚙️ CLI (コマンドライン) から使用

```bash
wintree /path/to/project --exclude .git __pycache__
```

#### オプション一覧

| オプション    | 説明                                                     |
| ------------- | -------------------------------------------------------- |
| path          | ルートディレクトリのパス                                 |
| --no-emoji    | 絵文字を非表示にする                                     |
| --exclude     | 除外するディレクトリ名（部分一致）をスペース区切りで指定 |
| --ext         | 検出したいファイル拡張子                                 |
| --no-tree     | ツリー状ではなく純粋なファイルパスを列挙する             |
| --abs         | ファイルパスの列挙を絶対パスにする                       |
| --json-output | JSON 形式でファイルの階層構造を保存するパス              |
| --show-meta   | JSON 出力時に日時やファイルサイズの情報も取得するか      |

## 📌 特長

- 絵文字によるツリー表示で視認性向上
- 除外対象のディレクトリを柔軟に指定可能
- Windows/macOS/Linux に対応
- Python のみで動作、外部依存なし

## 🧪 開発者向け

このライブラリはディレクトリ構造の可視化ツールのベースとしても応用可能です。GUI ツールや IDE プラグインとの統合も検討可能です。

## 📄 ライセンス

MIT License
