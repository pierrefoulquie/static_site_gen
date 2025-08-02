import os
import re
from enum_types import TextType, BlockType
from htmlnode import LeafNode, ParentNode, TextNode

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
                        alt_text = re.findall(alt_text_pattern, temp_node)[0].strip()
                        url = re.findall(url_pattern, temp_node)[0].strip()
                        if (alt_text != ""
                                and url != ""):
                            new_nodes_list.append(TextNode(alt_text, TextType.IMAGE, url))
                        else:
                            new_nodes_list.append(TextNode(temp_node, TextType.TEXT))

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
                        anchor = re.findall(anchor_pattern, temp_node)[0].strip()
                        url = re.findall(url_pattern, temp_node)[0].strip()
                        if (anchor != ""
                                and url != ""):
                            new_nodes_list.append(TextNode(anchor, TextType.LINK, url))
                        else:
                            new_nodes_list.append(TextNode(temp_node, TextType.TEXT))
                    else:
                        new_nodes_list.append(TextNode(temp_node, TextType.TEXT))
    return new_nodes_list

def text_to_textnodes(text):
    text_nodes = (split_nodes_image((split_nodes_link([TextNode(text, TextType.TEXT)]))))
    for text_type in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        text_nodes = split_nodes_delimiter(text_nodes, text_type.value["delim"], text_type)
    return text_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = list()
    for b in blocks:
        if b != "":
            clean_blocks.append(b.strip())
    return clean_blocks
    
def block_to_block_type(block):
    if re.match(r'^\#{1,6} ', block):
        return BlockType.HEADING
    elif block.strip()[:3] == "```" and block.strip()[-3:] == "```":
        return BlockType.CODE

    multi_lines = block.split("\n")

    q = 0
    u = 0
    o = 0
    num = 0
    for line in multi_lines:
        if re.match(r'^>', line.lstrip()):
            q += 1
        elif re.match(r'^- ', line.lstrip()):
            u += 1
        elif re.match(r'^\d+\. ', line.lstrip()):
            o += 1
        num += 1
    if q == num:
        return BlockType.QUOTE
    elif u == num:
        return BlockType.UNORDERED_LIST
    elif o == num:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def get_heading_level(heading):
    level = 0
    for c in heading:
        if c == "#":
            level += 1
    return level

def get_tag_and_text(block, block_type):
    if block_type == BlockType.HEADING:
        #for headings, build tag (h + level) and format text
        level = get_heading_level(block)
        tag = block_type.value["delim"] + str(level)
        text = " ".join(block[level:].splitlines()).strip()
    else:
        #generic tag
        tag = block_type.value["delim"]
    #text formating for non list block types
    if block_type == BlockType.PARAGRAPH:
        text = " ".join(block.splitlines()).strip()
    elif block_type == BlockType.CODE:
        text = block[3:-3]
    #text formating for quotes 
    elif block_type == BlockType.QUOTE:
        text = list()
        lines = block.splitlines()
        for line in lines:
            text.append(line[1:].strip())
        text = "\n".join(text)
    #text formating for lists 
    elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
        text = list()
        lines = block.splitlines()
        for line in lines:
            #get marker lenght by finding first whitespace
            first_blank = 0
            for i, c in enumerate(line):
                if c == " ":
                    first_blank = i
                    break
            text.append(f"<{block_type.value["inside_delim"]}>{line[first_blank:].strip()}</{block_type.value["inside_delim"]}>")
        text = "".join(text)
    return (tag, text)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = list()
    for block in blocks:
        block_types.append(block_to_block_type(block))

    tag_n_texts = list()
    for b, bt in zip(blocks, block_types):
        tag_n_texts.append(get_tag_and_text(b, bt))
    
    text_nodes = list()
    for text in tag_n_texts:
        text_nodes.append((text_to_textnodes(text[1]), text[0]))

    parents_nodes = list()
    for node in text_nodes:
        children_list = list()
        for child in node[0]:
            children_list.append(text_node_to_html_node(child))
        parents_nodes.append(ParentNode(node[1], children_list))
    div_node = ParentNode("div", parents_nodes)
    return div_node.to_html()

def extract_title(markdown):
    lines = str(markdown).splitlines()
    for line in lines:
        if re.match(r'^# ', line):
            return line.lstrip("#").strip()
    raise Exception("No h1 heading found")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating from {from_path}\n to {dest_path}\n using {template_path}.")
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"{from_path} file doesn't exist.")
    elif not os.path.exists(template_path):
        raise FileNotFoundError(f"{template_path} file doesn't exist.")

    dir_content = os.listdir(from_path)
    for content in dir_content:
        elt = os.path.join(from_path, content)
        if os.path.isfile(elt) and content.endswith(".md"):
            with open(elt, "r") as from_file:
                file_content = from_file.read()

            with open(template_path, "r") as template_file:
                template_content = template_file.read()
            
            html_content = markdown_to_html_node(file_content)

            title = extract_title(file_content)
            page_content = (template_content.replace("{{ Title }}", title)).replace("{{ Content }}", html_content)

            dest_file_path = os.path.join(dest_path, f"{os.path.splitext(content)[0]}.html")
            with open(dest_file_path, "w") as dest_file:
                dest_file.write(page_content)

        elif os.path.isdir(elt):
            new_dest = os.path.join(dest_path, content)
            if not os.path.exists(new_dest):
                os.mkdir(new_dest)
            generate_page(elt, template_path, new_dest)

