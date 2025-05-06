import os
from markdown_blocks import markdown_to_html_node, extract_title 

from_path = "../content/index.md"
template_path = "../template.html"
dest_path = "../public/index.html"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page form {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    if os.path.isfile(from_path): 
        file_obj = open(from_path)
        markdown = file_obj.read()
    else: 
        raise ValueError(f"path is not a file: {from_path}")
    if os.path.isfile(template_path):
        template_obj = open(template_path)
        template = template_obj.read()
    else: 
        raise ValueError(f"path is not a file: {template_path}")

    node = markdown_to_html_node(markdown)

    html_string = node.to_html()

    title = extract_title(markdown)

    # print(template)
    # print(title)
    # print(html_string)

    new_html_page = template.replace("Title", title, 1).replace("Content", html_string, 1)

    print(new_html_page)


generate_page(from_path, template_path, dest_path)





