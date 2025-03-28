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


class TestBlockToMarkdownType(unittest.TestCase):
    def test_block_to_block_type(self):
        md = """
# This is an H1 Heading
## This is an H2 Heading
### This is an H3 Heading

This is a paragraph in Markdown. It can span multiple lines and will be rendered as a single block of text.

```python 
inline code
```

> This is a blockquote.
> It can span multiple lines.

- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
- Item 3

1. First item
2. Second item
   1. Subitem 2.1
   2. Subitem 2.2
3. Third item
"""
        blocks = markdown_to_blocks(md)
        blocks_type = list(map(block_to_block_type, blocks))
        self.assertListEqual(
            [
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
            ],
            blocks_type
        )
