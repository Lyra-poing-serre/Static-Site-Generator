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
        self.children = children
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
        return f'href="{self.props["href"]}" target="{self.props["target"]}"'

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, *, value: str, tag: str = None, props: dict = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
