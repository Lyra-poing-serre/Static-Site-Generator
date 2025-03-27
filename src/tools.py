import re
from .textnode import TextNode, TextType
from .htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid type.")


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


def text_to_textnodes(text: str):
    out_nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)]:
        out_nodes = split_nodes_delimiter(out_nodes, delimiter, text_type)
    out_nodes = split_nodes_image(out_nodes)
    out_nodes = split_nodes_link(out_nodes)
    return out_nodes
