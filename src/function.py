import re
from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode

def text_node_to_html_node(text_node):
    if text_node.textType == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.textType == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.textType == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.textType == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.textType == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    elif text_node.textType == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})

def is_num_delimiter_even(string, delimiter):
    count = 0
    len_delim = len(delimiter)
    len_string = len(string)
    remaining_chars = 0
    for i in range(len_string):
        if remaining_chars > 0:
            remaining_chars -= 1
        elif string[i:i+len_delim] == delimiter:
            count+=1
            remaining_chars = len_delim - 1

    if count%2 ==0:
        return True
    return False

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = list()
    for old_node in old_nodes:
        if old_node.textType != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            if not is_num_delimiter_even(old_node.text, delimiter):
                raise SyntaxError("Odd number of delimiters")

            new_node = list()
            inside = False

            old_strings = old_node.text.split(delimiter)
            is_first_char_delimiter = old_node.text[:len(delimiter)] == delimiter
            if is_first_char_delimiter:
                inside = True

            for old_string in old_strings:
                if old_string == "":
                    pass
                elif inside == True:
                    new_node.append(TextNode(old_string, text_type))
                    inside = False
                elif inside == False:
                    new_node.append(TextNode(old_string, TextType.TEXT))
                    inside = True
            new_nodes.extend(new_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)

def split_nodes_image(old_nodes):
    image_pattern = re.compile(r'(!\[[^\[\]]*\]\([^\(\)]*\))')
    alt_text_pattern = re.compile(r'!\[([^\[\]]*)\]')
    url_pattern = re.compile(r'\(([^\(\)]*)\)')

    new_nodes_list = list()

    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes_list.append(node)
        else:
            temp_node_list = re.split(image_pattern, node.text)
            for temp_node in temp_node_list:
                if temp_node != "":
                    if re.match(image_pattern, temp_node):
                        alt_text = re.findall(alt_text_pattern, temp_node)[0]
                        url = re.findall(url_pattern, temp_node)[0]
                        new_nodes_list.append(TextNode(alt_text, TextType.IMAGE, url))
                    else:
                        new_nodes_list.append(TextNode(temp_node, TextType.TEXT))
    return new_nodes_list

def split_nodes_link(old_nodes):
    link_pattern = re.compile(r'((?<!!)\[[^\[\]]*\]\([^\(\)]*\))')
    anchor_pattern = re.compile(r'(?<!!)\[([^\[\]]*)\]')
    url_pattern = re.compile(r'\(([^\(\)]*)\)')

    new_nodes_list = list()

    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes_list.append(node)
        else:
            temp_node_list = re.split(link_pattern, node.text)
            for temp_node in temp_node_list:
                if temp_node != "":
                    if re.match(link_pattern, temp_node):
                        anchor = re.findall(anchor_pattern, temp_node)[0]
                        url = re.findall(url_pattern, temp_node)[0]
                        new_nodes_list.append(TextNode(anchor, TextType.LINK, url))
                    else:
                        new_nodes_list.append(TextNode(temp_node, TextType.TEXT))
    return new_nodes_list
