import unittest
from enum_types import TextType, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode, TextNode
from function import (split_nodes_delimiter,
        is_num_delimiter_even,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_link,
        split_nodes_image,
        text_to_textnodes,
        markdown_to_blocks,
        block_to_block_type,
        get_tag_and_text,
        markdown_to_html_node,
        extract_title)

class TestGetTagAndText(unittest.TestCase):
    def testParagraph(self):
        paragraph = """this is a paragraph"""
        result = get_tag_and_text(paragraph, BlockType.PARAGRAPH)
        model = ("p", "this is a paragraph")
        self.assertEqual(result, model)

    def testHeading1(self):
        heading = "#this is a h1 heading"
        result = get_tag_and_text(heading, BlockType.HEADING)
        model = ("h1", "this is a h1 heading")
        self.assertEqual(result, model)

    def testHeading2(self):
        heading = "##this is a h2 heading"
        result = get_tag_and_text(heading, BlockType.HEADING)
        model = ("h2", "this is a h2 heading")
        self.assertEqual(result, model)

    def testCode(self):
        code = """```this is
a code
block```"""
        result = get_tag_and_text(code, BlockType.CODE)
        model = ("code", "this is\na code\nblock")
        self.assertEqual(result, model)

    def testQuote(self):
        quote = """>this is
>a quote 
>block"""
        result = get_tag_and_text(quote, BlockType.QUOTE)
        model = ("blockquote", "this is\na quote\nblock")
        self.assertEqual(result, model)

    def testUnordered(self):
        unordered = """- this is
- an unordered 
- list"""
        result = get_tag_and_text(unordered, BlockType.UNORDERED_LIST)
        model = ("ul", "<li>this is</li><li>an unordered</li><li>list</li>")
        self.assertEqual(result, model)

    def testOrdered(self):
        ordered = """1. this is
2. an ordered 
3. list"""
        result = get_tag_and_text(ordered, BlockType.ORDERED_LIST)
        model = ("ol", "<li>this is</li><li>an ordered</li><li>list</li>")
        self.assertEqual(result, model)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://github.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_content_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an other text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_typ_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_meth(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(True, node==node2)

    def test_repr_meth(self):
        node = TextNode("This is a text node", TextType.BOLD)
        test_string = "TextNode(This is a text node, TextType.BOLD)"
        self.assertEqual(test_string, node.__repr__())

class TestEvenDelimiterFunc(unittest.TestCase):
    def test_odd_delimiters(self):
        result = is_num_delimiter_even("this is' a string ' with ' odd number of delimiters", "'")
        self.assertEqual(result, False)

    def test_even_delimiters(self):
        result = is_num_delimiter_even("this is*** a string with an even** number **of** delimiters", "**")
        self.assertEqual(result, True)

class TestSplitDelimiterFunc(unittest.TestCase):
    def test_trick_bold_case(self):
        node = TextNode("AA**BB**CC", TextType.TEXT)
        node1 = TextNode("hello****world", TextType.BOLD)
        node2 = TextNode("**foo**bar", TextType.BOLD)
        node3 = TextNode("**first**middle**last**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1, node2, node3], "**", TextType.BOLD)
        model_new_nodes = [
            TextNode("AA", TextType.TEXT),
            TextNode("BB", TextType.BOLD),
            TextNode("CC", TextType.TEXT),
            TextNode("hello****world", TextType.BOLD),
            TextNode("**foo**bar", TextType.BOLD),
            TextNode("first", TextType.BOLD),
            TextNode("middle", TextType.TEXT),
            TextNode("last", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_no_text_nodes(self):
        node = TextNode("This is not a TEXT node", TextType.ITALIC)
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "`", TextType.CODE)
        model_new_nodes = [
            TextNode("This is not a TEXT node", TextType.ITALIC),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_two_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "`", TextType.CODE)
        model_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_whole_string_delimited(self):
        node = TextNode("_All this string is between delimiters_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        model_new_nodes = [
            TextNode("All this string is between delimiters", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        model_new_nodes = [
            TextNode("This is text with no delimiter", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_multiple_char_delimiter(self):
        node = TextNode("This is text with **bold** content", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        model_new_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" content", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, model_new_nodes)

    def test_odd_num_delimiters(self):
        node = TextNode("This is text with **bold content", TextType.TEXT)
        with self.assertRaises(SyntaxError) as context:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), 'Odd number of delimiters')

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        model_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        images = extract_markdown_images(text)
        self.assertEqual(model_list, images)

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        model_list = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        links = extract_markdown_links(text)
        self.assertEqual(model_list, links)

    def test_avoid_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        model_list = []
        links = extract_markdown_images(text)
        self.assertEqual(model_list, links)

    def test_avoid_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        model_list = []
        links = extract_markdown_links(text)
        self.assertEqual(model_list, links)

    def test_empty_text(self):
        text = "![](https://images.com/img.png) and [](/href)"
        model_links = [("", "/href")]
        model_images = [("", "https://images.com/img.png")]
        result_links = extract_markdown_links(text)
        result_images = extract_markdown_images(text)
        self.assertEqual((model_links, model_images), (result_links, result_images))

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        model = [ TextNode("This is text with an ", TextType.TEXT),
                 TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                 TextNode(" and another ", TextType.TEXT),
                 TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),]
        self.assertListEqual(new_nodes, model)

    def test_split_images_empty_url(self):
        node = TextNode(
            "This is text with an ![image]() and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        model = [ TextNode("This is text with an ", TextType.TEXT),
                 TextNode("![image]()", TextType.TEXT),
                 TextNode(" and another ", TextType.TEXT),
                 TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),]
        self.assertListEqual(new_nodes, model)

    def test_split_images_blank_chars(self):
        node = TextNode(
            "This is text with an ![image](  https://i.imgur.com/zjjcJKZ.png  ) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        model = [ TextNode("This is text with an ", TextType.TEXT),
                 TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                 TextNode(" and another ", TextType.TEXT),
                 TextNode( "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),]
        self.assertListEqual(new_nodes, model)

    def test_split_images_faulty_syntax(self):
        node = TextNode("![first](url1![second](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        model = [TextNode("![first](url1", TextType.TEXT),
                 TextNode( "second", TextType.IMAGE, "url2"),]
        self.assertListEqual(new_nodes, model)

    def test_split_images_avoid_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        model = [ TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),]
        self.assertListEqual(new_nodes, model)

    def test_split_links(self):
        old_nodes = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )]
        test = split_nodes_link(old_nodes)
        model = [ TextNode("This is text with a link ", TextType.TEXT),
                 TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                 TextNode(" and ", TextType.TEXT),
                 TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),]
        self.assertEqual(test, model)

    def test_split_links_empty_url(self):
        node = TextNode(
            "This is text with a link [to boot dev]() and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        model = [ TextNode("This is text with a link ", TextType.TEXT),
                 TextNode("[to boot dev]()", TextType.TEXT),
                 TextNode(" and ", TextType.TEXT),
                 TextNode( "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),]
        self.assertListEqual(new_nodes, model)

    def test_split_links_avoid_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        model = [ TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),]
        self.assertListEqual(new_nodes, model)

    def test_split_links_empty_string(self):
        old_nodes = [TextNode(
            "",
            TextType.TEXT,
        )]
        test = split_nodes_link(old_nodes)
        model = []
        self.assertEqual(test, model)

class TestTextToTextNodes(unittest.TestCase):
    def test_image_and_links(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        model_nodes = [(TextNode("This is ", TextType.TEXT)),
                       (TextNode("text", TextType.BOLD)),
                       (TextNode(" with an ", TextType.TEXT)),
                       (TextNode("italic", TextType.ITALIC)),
                       (TextNode(" word and a ", TextType.TEXT)),
                       (TextNode("code block", TextType.CODE)),
                       (TextNode(" and an ", TextType.TEXT)),
                       (TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")),
                       (TextNode(" and a ", TextType.TEXT)),
                       (TextNode("link", TextType.LINK, "https://boot.dev")),
                       ]
        self.assertListEqual(text_nodes, model_nodes)

class TestMarkdownToBlocks(unittest.TestCase):
    def testMarkdownToBlocksEmpty(self):
        markdown = ""
        model = []
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(model, blocks)

    def testMarkdownToBlocksBasic(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        model = ["# This is a heading",
                 "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                 "- This is the first list item in a list block\n- This is a list item\n- This is another list item"]
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(model, blocks)

class TestBlockToBlockTypes(unittest.TestCase):
    def test_heading_block(self):
        block = "#### this is a heading"
        result = block_to_block_type(block)
        model = BlockType.HEADING
        self.assertEqual(result, model)

    def test_code_block(self):
        block = """```this is a first line of code
and this is the second```"""
        result = block_to_block_type(block)
        model = BlockType.CODE
        self.assertEqual(result, model)

    def test_quote_block(self):
        block = """>this is a quote
>this is still the same quote
>and here ends the quote"""
        result = block_to_block_type(block)
        model = BlockType.QUOTE
        self.assertEqual(result, model)

    def test_unordered_block(self):
        block = """- this is an unordered list
- this is the second element
- and this one is the third
- this one is the last"""
        result = block_to_block_type(block)
        model = BlockType.UNORDERED_LIST
        self.assertEqual(result, model)

    def test_ordered_block(self):
        block = """1. this is an ordered list
2. this is the second element
3. this is the third element
4. this is the last element"""
        result = block_to_block_type(block)
        model = BlockType.ORDERED_LIST
        self.assertEqual(result, model)

    def test_paragraph_block(self):
        block = """this is a simple paragraph block
with two lines"""
        result = block_to_block_type(block)
        model = BlockType.PARAGRAPH
        self.assertEqual(result, model)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def testBasic(self):
        markdown = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        result =  markdown_to_html_node(markdown)
        model = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(result, model)

    def testBigHeading(self):
        markdown = "#    Big Heading  "
        result =  markdown_to_html_node(markdown)
        model = "<div><h1>Big Heading</h1></div>"
        self.assertEqual(result, model)

    def testMultiLine(self):
        markdown = """This is
a multi-line


paragraph with 



strange spacing."""
        result =  markdown_to_html_node(markdown)
        model = "<div><p>This is a multi-line</p><p>paragraph with</p><p>strange spacing.</p></div>"
        self.assertEqual(result, model)

    def testOrderedList(self):
        markdown = """1. First
3. Third
7. Seventh"""
        result =  markdown_to_html_node(markdown)
        model = "<div><ol><li>First</li><li>Third</li><li>Seventh</li></ol></div>"
        self.assertEqual(result, model)

    def testListWithSpaces(self):
        markdown = """-   Item one   
- Item two
-    Item three"""
        result =  markdown_to_html_node(markdown)
        model = "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>"
        self.assertEqual(result, model)

class TestExtractTitle(unittest.TestCase):
    def testBasic(self):
        title = "# This is a title"
        result = extract_title(title)
        model = "This is a title"
        self.assertEqual(result, model)

    def testNoHeading(self):
        title = ">This is a title"
        with self.assertRaises(Exception) as context:
            result = extract_title(title)
        self.assertEqual(str(context.exception), "No h1 heading found")


if __name__ == "__main__":
    unittest.main()
