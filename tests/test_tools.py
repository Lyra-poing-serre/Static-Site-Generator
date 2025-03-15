import unittest
from src.textnode import TextType, TextNode
from src.htmlnode import LeafNode
from src.tools import text_node_to_html_node
from collections import OrderedDict


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self) -> None:
        node = TextNode("This is a text node.", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "This is a text node.")

    def test_bold(self) -> None:
        node = TextNode("This is a bold node.", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is a bold node.</b>")

    def test_italic(self) -> None:
        node = TextNode("This is a italic node.", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>This is a italic node.</i>")

    def test_code(self) -> None:
        node = TextNode("print('Hello World !')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello World !')</code>")

    def test_link(self) -> None:
        node = TextNode(
            "This is a link.",
            TextType.LINK,
            "https://www.google.com",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.google.com">This is a link.</a>',
        )

    def test_image(self) -> None:
        node = TextNode("Title", TextType.IMAGE, "/path/to/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="/path/to/image.png" alt="Title"></img>',
        )
