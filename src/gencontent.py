import os
import shutil
from markdown_blocks import markdown_to_html_node


# def generate_page(from_path, template_path, dest_path, basepath):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
#     markdown = ""
#     template = ""
#     if os.path.isfile(from_path): 
#         file_obj = open(from_path)
#         markdown = file_obj.read()
#         file_obj.close()
#     else: 
#         raise ValueError(f"path is not a file: {from_path}")
#     if os.path.isfile(template_path):
#         template_obj = open(template_path)
#         template = template_obj.read()
#     else: 
#         raise ValueError(f"path is not a file: {template_path}")
#
#     node = markdown_to_html_node(markdown)
#
#     html_string = node.to_html()
#
#     title = extract_title(markdown)
#
#     new_html_page = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html_string, 1)
#
#     with open(dest_path, "w") as file:
#         file.write(new_html_page)
    
def generate_page(from_path, template_path, to_path, basepath):
    print(f"Generating page from {from_path} to {to_path} using {template_path}")

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
    
    print(f"BASEPATH: {basepath}")

    final_html = template.replace("{{ Title }}", title, 1)
    final_html = final_html.replace("{{ Content }}", html_content, 1)
    html_basepath = final_html.replace('href="/', f'href="{basepath}')
    html_basepath = html_basepath.replace('src="/', f'src="{basepath}')

    file = open(to_path, "w")
    file.write(html_basepath)
    file.close()

    # markdown = ""
    # template = ""
    # if os.path.isfile(from_path): 
    #     file_obj = open(from_path)
    #     markdown = file_obj.read()
    #     file_obj.close()
    # else: 
    #     raise ValueError(f"path is not a file: {from_path}")
    # if os.path.isfile(template_path):
    #     template_obj = open(template_path)
    #     template = template_obj.read()
    # else: 
    #     raise ValueError(f"path is not a file: {template_path}")
    #
    # node = markdown_to_html_node(markdown)
    #
    # html_string = node.to_html()
    #
    # title = extract_title(markdown)
    #
    # new_html_page = template.replace("{{ Title }}", title, 1).replace("{{ Content }}", html_string, 1)
    #
    # with open(dest_path, "w") as file:
    #     file.write(new_html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
       
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry) 
        to_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(from_path) and entry.endswith(".md"):
            generate_page(from_path, template_path, to_path, basepath)
            # to_path = to_path.replace(".md", ".html", 1)
            # print(f" * {from_path} -> {to_path}")
            # file_obj = open(from_path, "r")
            # markdown = file_obj.read()
            # file_obj.close()
            #
            # title = extract_title(markdown)
            #
            # node = markdown_to_html_node(markdown)
            # html_content = node.to_html()
            #
            # template_obj = open(template_path, "r")
            # template = template_obj.read()
            # template_obj.close()
            #
            # final_html = template.replace("{{ Title }}", title, 1)
            # final_html = final_html.replace("{{ Content }}", html_content, 1)
            #
            #
            # file = open(to_path, "w")
            # file.write(final_html)
            # file.close()
        else:
            generate_pages_recursive(from_path, template_path, to_path, basepath)
            


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






