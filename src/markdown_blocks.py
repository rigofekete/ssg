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
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading format {block}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children) 

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    # safety check condition (we already confirmed the block type in type_to_html_node
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError(f"Invalid code block format, missign ``` delimiter: {block}")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])
    
def quote_to_html_node(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote format, missing starting '>'")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_to_html_node(block):
    html_items = []
    lists = block.split("\n")
    for list in lists:
        text = list[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def ol_to_html_node(block):
    html_items = []
    lists = block.split("\n")
    for list in lists:
        text = list[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
    


