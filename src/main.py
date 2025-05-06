import os
import shutil
from copystatic import cpy_static_to_public
from textnode import TextNode, TextType


static_path = "../static"
public_path = "../public"

def main():
    if os.path.exists(public_path):
        print(f"Removing path: {public_path}")
        shutil.rmtree(public_path)
    
    print("Copying static files to public directory...")
    cpy_static_to_public(public_path, static_path)


if __name__ == "__main__":
    main()
    

