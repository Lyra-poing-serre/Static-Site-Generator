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


def block_to_block_type(block: str):
    pass
