from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('method implemented in children classes')

    def props_to_html(self):
        html_str = ""
        if self.props != None:
            for k,v in self.props.items():
                html_str += f' {k}="{v}"'
            return html_str
        return None

    def __eq__(self, o):
        if (
            type(self) == type(o)
            and self.tag == o.tag
            and self.value == o.value
            and self.children == o.children
            and self.props_to_html() == o.props_to_html()
        ):
                return True
        return False

    def __repr__(self):
        return f"HTMLNode (\n tag : {self.tag}\n value : {self.value}\n children : {self.children}\n props : {self.props_to_html()}\n)"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode (\n tag : {self.tag}\n value : {self.value}\n props :{self.props_to_html()}\n)"

    def __eq__(self, o):
        if (
            self.tag == o.tag
            and self.value == o.value
            and self.props == o.props
        ):
            return True
        return False

    def to_html(self):
        if self.value == None:
            raise ValueError('attribute "value" missing')
        if self.tag == None:
            return self.value
        first_tag = self.tag
        if self.props != None:
            first_tag += self.props_to_html()
        return f"<{first_tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children ,props=None):
        super().__init__(tag, value=None, children=children, props=props)
            
    def to_html(self):
        if self.tag == None:
            raise ValueError('attribute "tag" missing')
        if self.children == None:
            raise ValueError('attribute "children" missing')
        first_tag = self.tag
        if self.props != None:
            first_tag += self.props_to_html()
        html_str = ""
        for child in self.children:
            html_str += child.to_html()
        return f"<{first_tag}>{html_str}</{self.tag}>"

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









