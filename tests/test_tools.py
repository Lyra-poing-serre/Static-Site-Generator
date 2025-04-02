import unittest

from src.tools import *


class TestExtractMarkdownTitle(unittest.TestCase):
    def test_normal_markdown(self):
        md = """
# Heading 1

## Heading 2

This is a paragraph with **bold** and _italic_ text.

> This is a blockquote with `code` in it.
"""
        title = extract_title(md)
        self.assertEqual("Heading 1", title)

    def test_error_markdown(self):
        md = """
        ## Heading 2

        This is a paragraph with **bold** and _italic_ text.

        > This is a blockquote with `code` in it.
        """
        with self.assertRaises(Exception):
            extract_title("")
            extract_title(md)
