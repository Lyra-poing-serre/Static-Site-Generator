import unittest

from src.markdown import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ],
        )


def test_markdown_to_blocks_heading(self):
    md = """
# This is a heading

    ## This is a second heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
"""
    blocks = markdown_to_blocks(md)
    self.assertListEqual(
        blocks,
        [
            "# This is a heading",
            "## This is a second heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ],
    )


def test_markdown_to_blocks_empty_markdown(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [""])
    with self.assertRaises(TypeError):
        markdown_to_blocks(None)
