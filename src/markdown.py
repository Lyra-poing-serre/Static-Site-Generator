import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list:
    if not isinstance(markdown, str):
        raise TypeError('Invalid type.')
    blocks = list(map(str.strip, markdown.split('\n\n')))
    return ["\n".join(list(map(str.strip, block.split('\n')))) for block in blocks]  # REMOVE trailing whitespace


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
