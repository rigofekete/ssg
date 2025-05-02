from enum import Enum 
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
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

