import unittest

from src.textnode import *
from src.tools import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT, "")
        node2 = TextNode("This is a text node", TextType.TEXT, "")
        self.assertEqual(node, node2)

    def test_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT, "")
        node2 = TextNode("This is a text", TextType.TEXT, "")
        node3 = TextNode("This is a text node", TextType.BOLD, "")
        node4 = TextNode("This is a text node", TextType.TEXT, "https://test.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_repr(self) -> None:
        text = "This is a text node"
        text_type = TextType.TEXT
        url = ""
        self.assertEqual(
            repr(TextNode(text, text_type, url)),
            f"TextNode({text}, {text_type.value}, {url})",
            "repr not equal",
        )

    def test_text(self) -> None:
        text = "This is a text node"
        node = TextNode(text, TextType.TEXT, "")
        self.assertIsInstance(node.text, str)
        self.assertEqual(node.text, text)

    def test_text_type(self) -> None:
        text_type = TextType.TEXT
        node = TextNode("This is a text node", text_type, "")
        self.assertIsInstance(node.text_type, TextType)
        self.assertEqual(node.text_type.value, text_type.value)

    def test_url(self) -> None:
        url = "https://test.com"
        node = TextNode("This is a text node", TextType.TEXT, url)
        self.assertIsInstance(node.url, str)
        self.assertEqual(node.url, url)


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

