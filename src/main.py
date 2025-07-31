from enum_types import TextType
from htmlnode import HTMLNode, LeafNode, TextNode
def main():
    leaf_node = LeafNode("a", "Click me!",{"href": "https://www.google.com"})

    print(leaf_node.children)

if __name__ == "__main__":
    main()
