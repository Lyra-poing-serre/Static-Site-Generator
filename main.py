from pathlib import Path
from os.path import dirname, abspath

from src.tools import copy_static_to_public, copy_content_dir


def main() -> None:
    root_dir = Path(dirname(abspath(__file__)))
    copy_static_to_public(root_dir)

    copy_content_dir(
        root_dir / 'content',
        root_dir / 'template.html',
        root_dir / 'public',
    )


if __name__ == "__main__":
    main()
