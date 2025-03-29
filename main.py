from src.textnode import TextNode, TextType
from src.tools import static_copy


def main() -> None:
    print(TextNode("Greedy goblin", TextType.LINK, "https://www.rexma.fr"))
    static_copy()


if __name__ == "__main__":
    main()
