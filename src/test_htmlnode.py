import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, TextNode
from textnode import TextType
from function import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    #equality
    def test_eq(self):
        node = HTMLNode("p", "the text inside a paragraph")
        node2 = HTMLNode("p", "the text inside a paragraph")
        self.assertEqual(node, node2)

    def test_child_eq(self):
        children1 = [HTMLNode("h1", "the text inside a heading1")]
        children2 = [HTMLNode("h1", "the text inside a heading1")]
        node = HTMLNode(children=children1)
        node2 = HTMLNode(children=children2)
        self.assertEqual(node, node2)

    #no equality
    def test_tag_not_eq(self):
        node = HTMLNode("h1", "the text inside a paragraph")
        node2 = HTMLNode("p", "the text inside a paragraph")
        self.assertNotEqual(node, node2)

    def test_content_not_eq(self):
        node = HTMLNode("h1", "the text inside a title")
        node2 = HTMLNode("h1", "the text inside a paragraph")
        self.assertNotEqual(node, node2)

    def test_child_not_eq(self):
        children1 = [HTMLNode("h1", "the text inside a heading1")]
        children2 = [HTMLNode("h2", "the text inside a heading2")]
        node = HTMLNode(children=children1)
        node2 = HTMLNode(children=children2)
        self.assertNotEqual(node, node2)

    #methods
    def test_repr_meth(self):
        node = HTMLNode("h1", "the text inside a paragraph")
        test_string = f"HTMLNode (\n tag : h1\n value : the text inside a paragraph\n children : None\n props : None\n)"
        self.assertEqual(test_string, node.__repr__())

    #no implementation
    def test_no_imp_to_html(self):
        node = HTMLNode("h1", "the text inside a paragraph")
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), 'method implemented in children classes')

class TestLeafNode(unittest.TestCase):
    #equality
    def test_eq(self):
        node = LeafNode("h1", "the text inside a header1")
        node2 = LeafNode("h1", "the text inside a header1")
        self.assertEqual(node, node2)

    def test_eq_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    #no equality
    def test_tag_not_eq(self):
        node = LeafNode("a", "Click me!")
        node2 = LeafNode("h1", "the text inside a header1")
        self.assertNotEqual(node, node2)

    def test_content_not_eq(self):
        node = LeafNode("h1", "Click me!")
        node2 = LeafNode("h1", "the text inside a header1")
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!", {"href": "https://www.github.com"})
        self.assertNotEqual(node, node2)

    #methods
    def test_to_html_meth(self):
        node = LeafNode("h1", "the text inside a header1")
        test_string = f"<h1>the text inside a header1</h1>"
        self.assertEqual(test_string, node.to_html())

    def test_repr_meth_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        test_string = f'LeafNode (\n tag : a\n value : Click me!\n props : href="https://www.google.com"\n)'
        self.assertEqual(test_string, node.__repr__())

    #no value
    def test_no_value(self):
        node = LeafNode("h1", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), 'attribute "value" missing')

class TestParentNode(unittest.TestCase):
    #methods
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context :
            parent_node.to_html()
        self.assertEqual(str(context.exception), 'attribute "children" missing')

    def test_to_html_with_props(self):
        parent_node = ParentNode(
            tag="div",
            children=[
                LeafNode("span", "This is a child!"),
                LeafNode(None, "And some plain text.")
            ],
            props={"class": "container", "style": "color:red;"}
        )
        self.assertEqual(parent_node.to_html(), '<div class="container" style="color:red;"><span>This is a child!</span>And some plain text.</div>')

class TestTextNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic_text(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code_text(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("Link to github", TextType.LINK, "https://github.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link to github")
        self.assertEqual(html_node.props, {"href":"https://github.com"})

    def test_img(self):
        node = TextNode("An ancient mystical scroll", TextType.IMAGE, "https://www.boot.dev/images/ancient_scroll.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.boot.dev/images/ancient_scroll.jpg","alt":"An ancient mystical scroll"})

if __name__ == "__main__":
    unittest.main()
