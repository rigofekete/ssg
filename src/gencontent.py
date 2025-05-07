import os
import shutil
from markdown_blocks import markdown_to_html_node

# since we are executing the program from the root with the main.sh script we need to set the paths according to the main.sh location (root)
from_path = "./content/index.md"
template_path = "./template.html"
dest_path = "./public/index.html"

dir_path_content = "./content"
dest_dir_path = "./public"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    if os.path.isfile(from_path): 
        file_obj = open(from_path)
        markdown = file_obj.read()
        file_obj.close()
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

    new_html_page = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html_string, 1)

    with open(dest_path, "w") as file:
        file.write(new_html_page)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
       
    print(f"DIR PATH CONTENT: {dir_path_content}")
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry) 
        to_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(from_path) and entry.endswith(".md"):
            to_path = to_path.replace(".md", ".html", 1)
            print(f" * {from_path} -> {to_path}")
            file_obj = open(from_path, "r")
            markdown = file_obj.read()
            file_obj.close()
            
            title = extract_title(markdown)

            node = markdown_to_html_node(markdown)
            html_content = node.to_html()

            template_obj = open(template_path, "r")
            template = template_obj.read()
            template_obj.close()

            final_html = template.replace("{{ Title }}", title, 1)
            final_html = final_html.replace("{{ Content }}", html_content, 1)

            file = open(to_path, "w")
            file.write(final_html)
            file.close()
        else:
            generate_pages_recursive(from_path, template_path, to_path)
            


# Rewrite this one 
# def extract_title(markdown):
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
#         if block[:2] == "# ":
#             header = block.split("\n")[0]
#             title = header[2:].strip()
#             return title
#     return None

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")


# generate_pages_recursive(dir_path_content, template_path, dest_dir_path)








