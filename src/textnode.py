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
    PARAGRAPH = {"type" : "paragraph",
                 "delim" : "p"}
    HEADING = {"type" : "heading",
               "delim" : "h"}
    CODE = {"type" : "code",
            "delim" : "code"}
    QUOTE = {"type" : "quote",
             "delim" : "blockquote"}
    UNORDERED_LIST = {"type" : "unordered",
                      "delim" : "ul",
                      "inside_delim" : "li"}
    ORDERED_LIST = {"type" : "ordered",
                    "delim" : "ol",
                    "inside_delim" : "li"}


