import sys
import os
import shutil

from copystatic import cpy_static_to_public
from gencontent import generate_pages_recursive

static_path = "./static"
public_path = "./docs"
content_path = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    print(f"Removing path: {public_path}")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    
    print("Copying static files to public directory...")
    cpy_static_to_public(public_path, static_path)

    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print("Generating pages.......")
    generate_pages_recursive(content_path, template_path, public_path, basepath)


if __name__ == "__main__":
    main()
    

