import os
import sys
sys.path.insert(0, "src")

from wintree import tree, list_files, tree_to_json

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.dirname(__file__))
    print(tree(root_dir=root_dir, use_emoji=True, ignore_dirs=[".git", "__pycache__"]))
    print("\n" + "-"*40 + "\n")
    print(list_files(root_dir=root_dir, ignore_dirs=[".git", "__pycache__"]))
    print("\n" + "-"*40 + "\n")
    print(tree_to_json(root_dir=root_dir, save_path="tree.json", ignore_dirs=[".git", "__pycache__"]))