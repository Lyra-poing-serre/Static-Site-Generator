from pathlib import Path
from os.path import dirname, abspath

from src.tools import copy_static_to_public, generate_page


def main() -> None:
    root_dir = Path(dirname(abspath(__file__)))
    copy_static_to_public(root_dir)

    generate_page(
        root_dir / 'content' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public' / 'index.html',
    )
    generate_page(
        root_dir / 'content' / 'contact' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public''content' / 'contact' / 'index.html',
    )
    generate_page(
        root_dir / 'content' / 'blog' / 'tom' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public' / 'blog' / 'tom' / 'index.html',
    )
    generate_page(
        root_dir / 'content' / 'blog' / 'majesty' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public' / 'blog' / 'majesty' / 'index.html',
    )
    generate_page(
        root_dir / 'content' / 'blog' / 'glorfindel' / 'index.md',
        root_dir / 'template.html',
        root_dir / 'public' / 'blog' / 'glorfindel' / 'index.html',
    )


if __name__ == "__main__":
    main()
