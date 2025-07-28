from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, textType, url = None):
        self.text = text
        self.textType = textType
        self.url = url

    def __eq__(self, o):
        if (
            type(self) == type(o)
            and self.text == o.text
            and self.textType == o.textType
            and self.url == o.url
        ):
                return True
        return False

    def __repr__(self):
        return(f"TextNode({self.text}, {self.textType.value}, {self.url})")

# def main():
#     text_node = TextNode("This is some anchor text", TextType.LINK, "https://github.com/pierrefoulquie/" )
#     print(text_node)
#
# if __name__ == "__main__":
#     main()
