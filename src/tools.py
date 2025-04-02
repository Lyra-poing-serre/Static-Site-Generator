import shutil
from pathlib import Path

from .markdown import markdown_to_html_node


def extract_title(markdown):
    all_nodes: list = markdown_to_html_node(markdown).children
    try:
        return list(
            filter(lambda node: node.tag == 'h1', all_nodes)
        )[0].children[0].value
    except IndexError:
        raise Exception('No title found')


def copy_static_to_public(root_dir):
    public_dir = root_dir / 'public'
    static_dir = root_dir / 'static'
    print(f'Deleting {public_dir}')
    shutil.rmtree(public_dir, ignore_errors=True)

    def copy_source(source_dir=static_dir, destination=public_dir):
        if isinstance(source_dir, str):
            source_dir = Path(source_dir).absolute()
        destination.mkdir(exist_ok=True)
        print(f'Copying {source_dir} to {destination}')
        for item in source_dir.iterdir():
            target_path = destination / item.name
            if item.is_file():
                shutil.copy(item, target_path)
            else:
                copy_source(item, target_path)

    print(f'Copying statics files into public dir.')
    copy_source()


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = from_path.read_text()
    template = template_path.read_text()
    nodes = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    new_page = template.format(Title=title, Content=nodes.to_html())

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.touch()
    dest_path.write_text(new_page)
