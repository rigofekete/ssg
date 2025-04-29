import unittest

from htmlnode import HTMLNode

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


