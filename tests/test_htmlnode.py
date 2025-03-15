from types import NoneType
import unittest

from src.htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self) -> None:
        self.assertEqual(HTMLNode(), HTMLNode())

    def test_repr(self) -> None:
        text = "Test"
        self.assertEqual(
            repr(HTMLNode(text)),
            f"HTMLNode({text}, {None}, {None}, {None})",
        )

    def test_tag(self) -> None:
        tag = "h1"
        node = HTMLNode(tag)
        self.assertIsInstance(node.tag, str)
        self.assertEqual(node.tag, tag)

    def test_value(self) -> None:
        value = "test"
        node = HTMLNode(value=value)
        self.assertIsInstance(node.value, str)
        self.assertEqual(node.value, value)

    def test_children(self) -> None:
        children = HTMLNode()
        node = HTMLNode(children=children)
        self.assertIsInstance(node.children, HTMLNode)
        self.assertEqual(node.children, children)

    def test_props(self) -> None:
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertIsInstance(node.props, dict)
        self.assertEqual(node.props, props)

    def test_to_html(self) -> None:
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_props_to_html(self) -> None:
        props = {"href": "https://www.google.com", "target": "_blank"}
        html = HTMLNode(props=props).props_to_html()
        self.assertIsInstance(html, str)
        self.assertEqual(html, f'href="{props["href"]}" target="{props["target"]}"')


class TestLeafNode(unittest.TestCase):
    def test_tag(self) -> None:
        tag = "b"
        node = LeafNode(tag=tag, value="")
        self.assertIsInstance(node.tag, str)
        self.assertEqual(node.tag, tag)

    def test_value(self) -> None:
        value = "test"
        node = LeafNode(tag="", value=value)
        self.assertIsInstance(node.value, str)
        self.assertEqual(node.value, value)

    def test_children(self) -> None:
        node = LeafNode(tag="", value="")
        self.assertIsInstance(node.children, NoneType)
        self.assertEqual(node.children, None)

    def test_props(self) -> None:
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode(tag="", value="", props=props)
        self.assertIsInstance(node.props, dict)
        self.assertEqual(node.props, props)

    def test_to_html(self) -> None:
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_props_to_html(self) -> None:
        props = {"href": "https://www.google.com", "target": "_blank"}
        html = LeafNode(tag="", value="", props=props).props_to_html()
        self.assertIsInstance(html, str)
        self.assertEqual(html, f'href="{props["href"]}" target="{props["target"]}"')
