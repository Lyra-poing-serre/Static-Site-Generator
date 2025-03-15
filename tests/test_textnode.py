import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)

    def test_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self) -> None:
        text = "This is a text node"
        text_type = TextType.NORMAL
        url = None
        self.assertEqual(
            repr(TextNode(text, text_type, url)),
            f"TextNode({text}, {text_type}, {url})",
        )

    def test_text(self) -> None:
        text = "This is a text node"
        node = TextNode(text, TextType.NORMAL)
        self.assertIsInstance(node.text, str)
        self.assertEqual(node.text, text)

    def test_text_type(self) -> None:
        text_type = TextType.NORMAL
        node = TextNode("This is a text node", text_type)
        self.assertIsInstance(node.text_type, TextType)
        self.assertEqual(node.text_type.value, text_type.value)

    def test_url(self) -> None:
        url = "https://test.com"
        node = TextNode("This is a text node", TextType.NORMAL, url)
        self.assertIsInstance(node.url, str)
        self.assertEqual(node.url, url)


if __name__ == "__main__":
    unittest.main()
