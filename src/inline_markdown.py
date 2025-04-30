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

           
        
