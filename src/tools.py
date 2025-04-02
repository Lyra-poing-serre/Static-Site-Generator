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


def copy_static_to_target(root_dir: Path, target: str):
    target_dir = root_dir / target
    static_dir = root_dir / 'static'
    print(f'Deleting {target_dir}')
    shutil.rmtree(target_dir, ignore_errors=True)

    def copy_source(source_dir=static_dir, destination=target_dir):
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


def copy_content_dir(*, from_path: Path, dest_path: Path, template_path: Path, base_path: str):
    template = template_path.read_text()

    def generate_page(source_dir: Path, destination_dir: Path):
        print(f"Generating page from {source_dir} to {dest_path} using {template_path}")
        for item in source_dir.iterdir():
            target_path = destination_dir / item.name
            if item.is_file():
                target_path = target_path.with_suffix('.html')
                markdown = item.read_text()
                nodes = markdown_to_html_node(markdown)
                title = extract_title(markdown)
                new_page = template.replace(
                    "{{ Title }}", title
                ).replace("{{ Content }}", nodes.to_html()
                          ).replace('href="/', f'href="{base_path}'
                                    ).replace('src="/', f'src="{base_path}')

                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.touch()
                target_path.write_text(new_page)
            else:
                generate_page(item, target_path)

    generate_page(from_path, dest_path)
