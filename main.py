from src.textnode import TextNode, TextType
from src.tools import copy_static_to_public


def main() -> None:
    print(TextNode("Greedy goblin", TextType.LINK, "https://www.rexma.fr"))
    copy_static_to_public()


if __name__ == "__main__":
    main()
