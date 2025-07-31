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

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "u"
    ORDERED_LIST = "o"
