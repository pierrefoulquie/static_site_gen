from enum import Enum

class TextType(Enum):
    TEXT = {"type" : "text",
            "delim": None}
    BOLD = {"type" : "bold",
            "delim" : "**"}
    ITALIC = {"type" : "italic",
              "delim" : "_"}
    CODE = {"type" : "code",
            "delim" : "`"}
    LINK = {"type" : "link"}
    IMAGE = {"type" : "image"}


class TextNode():
    def __init__(self, text, textType, url=None):
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
        if self.url == None:
            return(f"TextNode({self.text}, {self.textType})")
        return(f"TextNode({self.text}, {self.textType}, {self.url})")

