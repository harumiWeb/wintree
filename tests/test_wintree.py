import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, "src")

import wintree

# tests/test_wintree.py


# Helpers
def create_structure(base: Path, structure: dict):
    """
    base/
      - "file.txt": "content"
      - "subdir": { ... nested ... }
    """
    for name, content in structure.items():
        path = base / name
        if isinstance(content, dict):
            path.mkdir()
            create_structure(path, content)
        else:
            path.write_text(content, encoding="utf-8")


class TestTreeFunction:
    def test_tree_basic_with_and_without_emoji(self, tmp_path):
        # ディレクトリ構造を作成
        structure = {
            "a.txt": "hello",
            "b.py": "print('hi')",
            "sub": {
                "c.md": "markdown"
            }
        }
        create_structure(tmp_path, structure)

        # 絵文字あり
        out = wintree.tree(str(tmp_path), use_emoji=True)
        # root ヘッダ
        assert out.splitlines()[0].startswith("📂 root:")
        # サブディレクトリとファイルが描画されている
        assert "└── 📁 sub/" in out
        assert "└── 📄 c.md" in out

        # 絵文字なし
        out_no_emoji = wintree.tree(str(tmp_path), use_emoji=False)
        assert "root:" in out_no_emoji
        assert "└── sub/" in out_no_emoji
        assert "└── c.md" in out_no_emoji

    def test_tree_ignore_dirs_and_filter_exts(self, tmp_path):
        structure = {
            "keep.txt": "ok",
            "__pycache__": {"ignored.pyc": ""},
            "foo.py": "print",
        }
        create_structure(tmp_path, structure)

        out = wintree.tree(
            str(tmp_path),
            ignore_dirs=["__pycache__"],
            filter_exts=[".txt"]
        )
        # __pycache__ 以下は無視
        assert "__pycache__" not in out
        # .txt のみ
        assert "keep.txt" in out
        assert "foo.py" not in out

    def test_tree_empty_directory(self, tmp_path):
        # 空ディレクトリ
        newdir = tmp_path / "empty"
        newdir.mkdir()
        out = wintree.tree(str(newdir))
        assert "(No files or directories found)" in out

    def test_tree_nonexistent_dir_raises(self):
        with pytest.raises(ValueError) as ei:
            wintree.tree("no_such_dir")
        assert "does not exist" in str(ei.value)


class TestListFilesFunction:
    def test_list_files_basic(self, tmp_path):
        structure = {
            "a.txt": "1",
            "sub": {"b.py": "2"},
        }
        create_structure(tmp_path, structure)

        out = wintree.list_files(str(tmp_path))
        lines = out.strip().splitlines()
        # Windows の絶対パス（バックスラッシュ）で返ってくる
        assert str(tmp_path / "a.txt") in lines
        assert str(tmp_path / "sub" / "b.py") in lines

    def test_list_files_ignore_dirs_and_filter_exts(self, tmp_path):
        structure = {
            "keep.log": "1",
            "drop.log": "2",
            "sub": {"c.txt": "3"},
        }
        create_structure(tmp_path, structure)

        out = wintree.list_files(
            str(tmp_path),
            ignore_dirs=["drop"],
            filter_exts=[".txt"]
        )
        lines = out.strip().splitlines()
        # drop.log は無視、.txt のみ
        assert any("drop.log" in p for p in lines) is False
        assert any("keep.log" in p for p in lines) is False
        assert any("c.txt" in p for p in lines)

    def test_list_files_nonexistent_dir_raises(self):
        with pytest.raises(ValueError):
            wintree.list_files("no_such_dir")


class TestTreeToJsonFunction:
    def test_tree_to_json_default_and_custom_save(self, tmp_path):
        # 1. ディレクトリ構造
        structure = {
            "f1.txt": "foo",
            "sub": {"f2.py": "bar"},
        }
        src = tmp_path / "src"
        src.mkdir()
        create_structure(src, structure)

        # デフォルト save_path
        res1 = wintree.tree_to_json(str(src), ignore_dirs=[], filter_exts=[])
        # 戻り値は dict
        assert isinstance(res1, dict)
        # デフォルトの JSON ファイルが作成される
        default_path = Path(str(src) + "_tree.json")
        assert default_path.exists()
        data_on_disk = json.loads(default_path.read_text(encoding="utf-8"))
        assert data_on_disk == res1

        # カスタム save_path
        custom = tmp_path / "outdir" / "mytree.json"
        res2 = wintree.tree_to_json(
            str(src),
            save_path=str(custom),
            ignore_dirs=[],
            filter_exts=[],
            show_meta=True
        )
        # JSON ファイル作成と読み込み
        assert custom.exists()
        loaded = json.loads(custom.read_text(encoding="utf-8"))
        assert loaded == res2
        # show_meta=True なのでファイル辞書に size, updated が含まれる
        file_nodes = [c for c in res2["children"] if c["type"] == "file"]
        assert file_nodes and "size" in file_nodes[0] and "updated" in file_nodes[0]

    def test_tree_to_json_exclude_dirs_and_filter_exts(self, tmp_path):
        structure = {
            "ok.py": "",
            "no.md": "",
            "drop": {"x.txt": ""}
        }
        base = tmp_path / "base"
        base.mkdir()
        create_structure(base, structure)
        out_json = tmp_path / "o.json"

        res = wintree.tree_to_json(
            str(base),
            save_path=str(out_json),
            ignore_dirs=["drop"],
            filter_exts=[".py"]
        )
        # drop 以下は無視
        names = {c["name"] for c in res["children"]}
        assert "drop" not in names
        # .py のみ
        assert "ok.py" in names
        assert "no.md" not in names

    def test_tree_to_json_invalid_save_path(self, tmp_path):
        src = tmp_path / "d"
        src.mkdir()
        with pytest.raises(ValueError) as ei:
            wintree.tree_to_json(str(src), save_path=str(tmp_path / "bad.txt"))
        assert "must end with '.json'" in str(ei.value)
