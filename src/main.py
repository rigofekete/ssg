import sys
import os
import shutil
from copystatic import cpy_static_to_public
from gencontent import generate_pages_recursive

# since we are executing the program from the root with the main.sh script we need to set the paths according to the main.sh location (root)
static_path = "./static"
public_path = "./docs"

content_path = "./content"
template_path = "./template.html"

# static_path = "../static"
# public_path = "../public"
#
# from_path = "../content"
# template_path = "../template.html"
# dest_path = "../public"

def main():
    if os.path.exists(public_path):
        print(f"Removing path: {public_path}")
        shutil.rmtree(public_path)
    
    print("Copying static files to public directory...")
    cpy_static_to_public(public_path, static_path)

    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"


    generate_pages_recursive(content_path, template_path, public_path, basepath)


if __name__ == "__main__":
    main()
    

