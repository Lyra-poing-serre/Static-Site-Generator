import unittest
from collections import OrderedDict
from src.htmlnode import HTMLNode, LeafNode, ParentNode


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
        props = OrderedDict(href="https://www.google.com", target="_blank")
        node = HTMLNode(props=props)
        self.assertIsInstance(node.props, dict)
        self.assertEqual(node.props, props)

    def test_to_html(self) -> None:
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

    def test_props_to_html(self) -> None:
        props = OrderedDict(href="https://www.google.com", target="_blank")
        html = HTMLNode(props=props).props_to_html()
        self.assertIsInstance(html, str)
        self.assertEqual(html, f' href="{props["href"]}" target="{props["target"]}"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self) -> None:
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self) -> None:
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(tag="p", children=children)
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self) -> None:
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        child = ParentNode(tag="p", children=children)
        node = ParentNode(tag="div", children=[child])
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>",
        )

    def test_to_html_with_children(self) -> None:
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(
            tag="p",
            children=children,
            props=OrderedDict(href="https://www.google.com", target="_blank"),
        )
        self.assertEqual(
            node.to_html(),
            '<p href="https://www.google.com" target="_blank"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )
