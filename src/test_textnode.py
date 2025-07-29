import unittest
from textnode import TextNode, TextType
from function import split_nodes_delimiter, is_num_delimiter_even, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image

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

if __name__ == "__main__":
    unittest.main()
