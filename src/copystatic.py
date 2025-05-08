import os
import shutil

def cpy_static_to_public(dest, src):
    if not os.path.exists(dest):
        os.mkdir(dest)

    print(f" LOG SRC: {src}")
    for filename in os.listdir(src):
        new_src_path = os.path.join(src, filename)
        new_dest_path = os.path.join(dest, filename)
        print(f" * {new_src_path} -> {new_dest_path}")
        if os.path.isfile(new_src_path):
            shutil.copy(new_src_path, new_dest_path)
        else:
            cpy_static_to_public(new_dest_path, new_src_path)


