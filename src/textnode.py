import re
from enum import Enum

from .htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target) -> bool:
        return all(
            (
                self.text == target.text,
                self.text_type == target.text_type,
                self.url == target.url,
            )
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    inline_value = re.sub(
        r'\s+', ' ',
        text_node.text
    )  # Replace all whitespace sequences with a single space
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, inline_value)
        case TextType.BOLD:
            return LeafNode("b", inline_value)
        case TextType.ITALIC:
            return LeafNode("i", inline_value)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid type.")


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_from_type(target_type: TextType):
    match target_type:
        case TextType.IMAGE:
            type_func = extract_markdown_images
            split_value = "![{}]({})"
        case TextType.LINK:
            type_func = extract_markdown_links
            split_value = "[{}]({})"
        case _:
            raise NotImplementedError('Invalid type')

    def split_node(old_nodes: list) -> list:
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            matches = type_func(old_node.text)
            if not matches:
                if old_node.text == '':
                    continue
                new_nodes.append(old_node)
                continue

            old_text = old_node.text
            for alt, link in matches:
                res = old_text.split(split_value.format(alt, link), 1)
                text = res.pop(0)
                if text != '':
                    new_nodes.append(TextNode(text, TextType.TEXT))
                new_nodes.append(TextNode(alt, target_type, link))
                old_text = res.pop()
            if old_text != '':
                new_nodes.append(TextNode(old_text, TextType.TEXT))

        return new_nodes

    return split_node


def split_nodes_image(old_nodes):
    return split_nodes_from_type(TextType.IMAGE)(old_nodes)


def split_nodes_link(old_nodes):
    return split_nodes_from_type(TextType.LINK)(old_nodes)
