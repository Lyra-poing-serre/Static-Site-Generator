class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children=None,
        props: dict = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children: list = children
        self.props = props

    def __eq__(self, target) -> bool:
        return all(
            (
                self.tag == target.tag,
                self.value == target.value,
                self.children == target.children,
                self.props == target.props,
            )
        )

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        elif self.children is None:
            raise ValueError("All parent nodes must have a children.")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
