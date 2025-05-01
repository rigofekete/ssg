import re 

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            # if type is not text we need to skip the rest of the logic because since we are not splitting non text types, they are ready to be added to the new nodes as they are.
            continue

        split_lines = []
        sections = []
        sections = node.text.split(delimiter)
        # if the list of split lines is even it means we have a delimiter without closure. Always remember that properly delimited splitted lines need to have an odd size (number of lines need to be 
        if len(sections) % 2 == 0:
            raise ValueError(f"no matching closing delimiter found: {delimiter}") 

        for i in range(0, len(sections)):
            # skip empty sections, no need to make text nodes out of them
            if sections[i] == "":
                continue
            # When delimiters are properly matched, split will always return an odd number of parts. That's because every delimiter splits the string, making one more piece than the total number of delimiters.
            # we check if index is even or odd to define which of the lines is outer delimited (even) and which ones are the delimited lines (odd)
            if i % 2 == 0:
                split_lines.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_lines.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_lines)

    return new_nodes




def split_nodes_images(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        # at each node iteration we extract its markdown images 
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for tuple in images:
            # Important! we split each section of the text separately for each tuple so we can create the TextNodes accordingly 
            sections = original_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
            # Remember that since we are splitting a string only once with the delimiter pattern, the resulting length needs to be 2 (2 split lines)! otherwise it means that we have an open [ or ( without a matching closing one
            if len(sections) != 2:
                raise ValueError(f"no matching closing delimiter found")
            # check if the first section is empty (for example if the string starts with the i tag or with [. If is is empty skip the TEXT type node and append the IMAGE type instead 
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
            # we place the second part of the full node text sting for it to be split in the next iteration in order to create the next TextNodes
            original_text = sections[1]
        # if eventually there is still some left over text after iterating all tuples, append it to the new nodes list 
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes 

def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for tuple in links:
            sections = original_text.split(f"[{tuple[0]}]({tuple[1]})", 1)
            if len(sections) != 2:
                raise ValueError(f"no matching closing delimiter found")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes 



def extract_markdown_images(text):
    # non-greedy match, will capture eventual inner [ and (, thats why the regex expression below is better 
    # matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    # matching any character except [ ] and ( ) 
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes 


