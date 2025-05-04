import unittest
from markdown_blocks import(
        markdown_to_blocks, 
        block_to_block_type,
        BlockType,
        markdown_to_html_node
     )


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # IMPORTANT, when defining a multiline string with """ we need to indent the block without leading whitespaces otherwise they will be part of the multiline string.  
        # This is why we indent it this way, no spaces before the start of each line
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = """

#### This is a level 4 heading

```
This is a level 4 heading 
```

> I`m a firestarter, twisted firestarter
> I`m a firestarter, twisted firestarter


- this is a list 
- with some errands
- for Nando to execute


1. an ordered list
2. with nothing useful
3. really



"""

        filtered_md = markdown_to_blocks(md)
        block_types = []
        for block in filtered_md:
            block_types.append(block_to_block_type(block))

        self.assertEqual(
                block_types,
                [
                    BlockType.HEADING,
                    BlockType.CODE,
                    BlockType.QUOTE,
                    BlockType.ULIST,
                    BlockType.OLIST,
                ]
        )

    def test_block_to_block_types_2(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
            block = "- list\n- items"
            self.assertEqual(block_to_block_type(block), BlockType.ULIST)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), BlockType.OLIST)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_headings(self):
        md = """


### this is a header


"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>this is a header</h3></div>"
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )











if __name__ == "__main__":
    unittest.main()
