import re
from enum import Enum

from .htmlnode import ParentNode, LeafNode, HTMLNode
from .tools import text_to_textnodes, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif block.startswith('>'):
        return BlockType.QUOTE
    elif block.startswith('- '):
        return BlockType.UNORDERED_LIST
    elif block.startswith('1. '):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_block_to_html_node(md_block: str, md_type: BlockType) -> HTMLNode:
    match md_type:
        case BlockType.PARAGRAPH:
            return ParentNode('p', children=children_to_html_node(md_block))
        case BlockType.HEADING:
            heading_level = min(len(md_block.split(' ')[0]), 6)  # Count the `#` before the first space
            heading_text = md_block.lstrip('#').strip()  # Remove leading `#` and trim spaces
            return ParentNode("h{}".format(heading_level), children=children_to_html_node(heading_text))
        case BlockType.CODE:
            return ParentNode("pre", children=[LeafNode('code', md_block.lstrip('```').rstrip('```').lstrip())])
        case BlockType.QUOTE:
            return ParentNode('blockquote', children=children_to_html_node(md_block.lstrip('>').strip()))
        case BlockType.UNORDERED_LIST:
            return ParentNode(
                "ul",
                children=[
                    ParentNode('li', children=children_to_html_node(child.strip()))
                    for child in md_block.split('- ') if child.strip()
                ]
            )
        case BlockType.ORDERED_LIST:
            return ParentNode(
                "ol",
                children=[
                    ParentNode('li', children=children_to_html_node(child.strip()))
                    for child in re.split(r'\d+\.\s', md_block) if child.strip()
                ]
            )
        case _:
            raise Exception("Invalid BlockType.")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    return ParentNode(
        'div',
        list(
            markdown_block_to_html_node(
                block, block_to_block_type(block)
            )
            for block in blocks
        )
    )


def children_to_html_node(markdown_children: str) -> list:
    nodes = text_to_textnodes(markdown_children)
    return list(map(text_node_to_html_node, nodes))


