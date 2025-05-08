import os

from pathlib import Path
from markdown_blocks import markdown_to_html_node
    
def generate_page(from_path, template_path, to_path, basepath):
    print(f" * {from_path} -> {to_path}")
    file_obj = open(from_path, "r")
    markdown = file_obj.read()
    file_obj.close()

    node = markdown_to_html_node(markdown)
    html_content = node.to_html()

    template_obj = open(template_path, "r")
    template = template_obj.read()
    template_obj.close()

    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title, 1)
    final_html = final_html.replace("{{ Content }}", html_content, 1)
    html_basepath = final_html.replace('href="/', f'href="{basepath}')
    html_basepath = html_basepath.replace('src="/', f'src="{basepath}')


    dest_dir_path = os.path.dirname(to_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    file = open(to_path, "w")
    file.write(html_basepath)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry) 
        to_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(from_path):
            to_path = Path(to_path).with_suffix(".html")
            generate_page(from_path, template_path, to_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, to_path, basepath)
            

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")






