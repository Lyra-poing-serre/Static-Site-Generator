import unittest

from src.Textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url():
        node = TextNode("This is a text node", TextType.BOLD)
        assert hasattr(node, "url")
        assert node.url is None


if __name__ == "__main__":
    unittest.main()
