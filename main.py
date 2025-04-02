import sys
from pathlib import Path
from os.path import dirname, abspath

from src.tools import copy_static_to_public, copy_content_dir


def main(base_path: str) -> None:
    root_dir = Path(dirname(abspath(__file__)))
    copy_static_to_public(root_dir)

    copy_content_dir(
        from_path=root_dir / 'content',
        dest_path=root_dir / 'docs',
        template_path=root_dir / 'template.html',
        base_path=base_path
    )


if __name__ == "__main__":
    base_path = sys.argv[-1]
    if not base_path or 'main.py' in base_path:
        base_path = '/'
    main(base_path)
