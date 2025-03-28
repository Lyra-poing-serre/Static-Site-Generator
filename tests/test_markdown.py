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
        self.assertEqual(blocks, [])
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


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Heading 1

## Heading 2

This is a paragraph with **bold** and _italic_ text.

> This is a blockquote with `code` in it.

- List item 1
- List item 2
- List item 3

1. Ordered item 1
2. Ordered item 2
3. Ordered item 3

```
def sample_code():
    return "This is a code block"
```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><blockquote>This is a blockquote with <code>code</code> in it.</blockquote><ul><li>List item 1</li><li>List item 2</li><li>List item 3</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li><li>Ordered item 3</li></ol><pre><code>def sample_code():\n    return \"This is a code block\"\n</code></pre></div>"
        )