from enum import Enum 
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH      = "paragraph"
    HEADING        = "heading"
    CODE           = "code"
    QUOTE          = "quote"
    ULIST          = "unordered_list"
    OLIST          = "ordered_list"
    
# MY VERSION, not sure if it handles all of the cases so I am using Lane's function instead 
# def block_to_block_type(block):
#     if re.findall(r"(^#{1,6}) .*?", block):
#         return BlockType.HEADING
#
#     if block[:3] == "```" and block[-3:] == "```":
#         return BlockType.CODE
#
#     if block[:1] == ">":
#         sections = block.split("\n")
#         for section in sections:
#           if section[:1] != ">":
#               return BlockType.PARAGRAPH
#         return BlockType.QUOTE
#
#     if block[:2] == "- ":
#         sections = block.split("\n")
#         for section in sections:
#             if section[:2] != "- ":
#                 return BlockType.PARAGRAPH
#         return BlockType.ULIST
#
#     if re.findall(r"(^\d. ).*?", block):
#         sections = block.split("\n")
#         index = int(sections[0][0])
#         for section in sections:
#             if (not re.findall(r"(^\d. ).*?", section)) or (int(section[0]) != index):
#                 return BlockType.PARAGRAPH
#             index = int(section[0]) + 1 
#
#         return BlockType.OLIST
#
#     return BlockType.PARAGRAPH

# LANE's version 
def block_to_block_type(block):
    lines = block.split("\n")
    # startswith also accepts a tuple with different prefixes to look for (like below), check python documentation 
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = type_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

        
def type_to_html_node(block):
    block_type = block_to_block_type(block)
    match(block_type):
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.ULIST:
            return ul_to_html_node(block)
        case BlockType.OLIST:
            return ol_to_html_node(block)
        case _:
            raise ValueError(f"invalid block type: {block_type}")
            
def text_to_children(text):
    children = []
    nodes = text_to_text_nodes(text)
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level = level + 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading format {block}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children) 

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)

def code_to_html_node(block):
    text = block.strip("```")
    text = text[1:]
    code_node = TextNode(text, TextType.CODE, None)
    html_node = text_node_to_html_node(code_node)
    return ParentNode("pre", [html_node])
    
def quote_to_html_node(block):
    children = []
    text = ""
    quotes = block.split("\n")
    for quote in quotes:
        if quote.startswith(">"):
            text += quote[1:]
        else:
            raise ValueError("invalid quote format, missing starting '>'")
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def ul_to_html_node(block):
    children = []
    text = ""
    lists = block.split("\n")
    for list in lists:
        text += f"<ls>{list[2:]}<ls>"
    children = text_to_children(text)
    return ParentNode("ul", children)

def ol_to_html_node(block):
    children = []
    text = ""
    lists = block.split("\n")
    for list in lists:
        text += f"<ls>{list[3:]}<ls>"
    children = text_to_children(text)
    return ParentNode("ol", children)
    




#
#
# md = """
#
# #### This is a level 4 heading
#
# ```
# This is a level 4 heading 
# ```
#
# > I`m a firestarter, twisted firestarter
# > I`m a firestarter, twisted firestarter
#
#
# - this is a list 
# - with some errands
# - for Nando to execute
#
#
# 1. an ordered list
# 2. with nothing useful
# 3. really
#
#
# """
#

# md = """
#
# ```
# this is a **paragraph** and I do not know what to do
# I also dont know what to write
# ```
# """

md = """

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""



# md = """
#
# > I am the god of hellfire and I bring you... fire.
# > quote unquote
#
# """

# md = """
#
# - eat lunch
# - drink coffee 
# - clean the bathroom
#
# """

# md = """
#
# 1. no coffee
# 2. no wine
# 3. maybe something sweet
# 4. hit the sack
#
# """

node = markdown_to_html_node(md)
# print(f"NODE: {node}")
html = node.to_html()

print(html)

