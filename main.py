import sys
from pathlib import Path
from os.path import dirname, abspath

from src.tools import copy_static_to_public, copy_content_dir

root_dir = Path(dirname(abspath(__file__)))

if __name__ == "__main__":
    base_path = sys.argv[0]
    print(sys.argv)
    if not base_path:
        base_path = '.'
    base_path = Path(base_path).resolve()
    # copy_static_to_public(base_path)
#
    # copy_content_dir(
    #     base_path / 'content',
    #     base_path / 'template.html',
    #     base_path / 'public',
    # )