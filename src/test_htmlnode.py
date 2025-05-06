import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node 

class TestHtmlNode(unittest.TestCase):
    def test_custom(self):
        print("Testing propr....\n")
        dict = {"href": "https://www.huha.hu", "target": "_blank"}
        node = HTMLNode(tag="<a>", props=dict)
        print(f"Node to be tested: \n{node}\n")
        print("Testing props_to_html()...")
        print(node.props_to_html())
        self.assertEqual(node.tag, "<a>")

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )

        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag: p, value: What a strange world, children: None, props: {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.pt"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.pt">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, jello!")
        self.assertEqual(node.to_html(), "Hello, jello!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
                parent_node.to_html(), 
                "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
        )
        self.assertEqual(
                node.to_html(),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_headings(self):
        node = ParentNode(
                "h2",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ]
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>"
        )

    def test_to_html_without_children(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
        parent_node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test__repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("span", [child_node])
        print(parent_node.__repr__())
        self.assertEqual(
                parent_node.__repr__(),
                "ParentNode(tag: span, children: [(LeafNode(span, child, None)], props: None)"
        )

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://macaco.io")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": node.url})

    def test_image(self):
        node = TextNode(
                "A human shaped scissors",
                TextType.IMAGE,
                "https://macaco.io/assets/evidence.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": node.text})


        
if __name__ == "__main__":
    unittest.main()

