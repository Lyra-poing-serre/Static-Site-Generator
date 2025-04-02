from pathlib import Path
from os.path import dirname, abspath

from src.tools import copy_static_to_public, generate_page


def main() -> None:
    root_dir = Path(dirname(abspath(__file__))).parent
    copy_static_to_public(root_dir)
    generate_page(
        root_dir / 'content' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public' / 'template.html',
    )


if __name__ == "__main__":
    main()
