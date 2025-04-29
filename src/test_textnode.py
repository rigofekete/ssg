import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is horrendus", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node = TextNode("", TextType.LINK, None);
        self.assertEqual(node.url, None)

    def test_eq_url_false(self):
        node = TextNode("", TextType.LINK, "http://whatever.com")
        self.assertNotEqual(node.url, None)

    def test_text_false(self):
        node = TextNode("This is rubbish", TextType.TEXT)
        node2 = TextNode("This is wicked", TextType.TEXT)
        self.assertNotEqual(node.text, node2.text)

    def test_eq_type(self):
        node = TextNode("No electricity", TextType.ITALIC)
        node2 = TextNode("At the drive in.", TextType.ITALIC)
        self.assertEqual(node.text_type, node2.text_type)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
                "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
                )
if __name__ == "__main__":
    unittest.main()
