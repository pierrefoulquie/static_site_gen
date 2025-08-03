import os
import sys
import shutil
from enum_types import TextType
from htmlnode import HTMLNode, LeafNode, TextNode
from function import generate_page

def main(basepath = "/"):
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    working_dir = os.getcwd()
    public_dir = os.path.join(working_dir, "docs")
    static_dir = os.path.join(working_dir, "static")
    initDirectories(public_dir, static_dir)
    copyDir(static_dir, public_dir)
    from_path = os.path.join(working_dir,"content")
    template_path = os.path.join(working_dir,"template.html")
    dest_path = public_dir
    generate_page(from_path, template_path, dest_path, basepath)



def initDirectories(public_dir, static_dir):
    if not os.path.exists(public_dir):
        os.mkdir(public_dir)
    if not os.path.exists(static_dir):
        os.mkdir(static_dir)

def copyDir(source, target):
    for elt in os.listdir(target):
        elt_path = os.path.join(target, elt)
        if os.path.isdir(elt_path):
            shutil.rmtree(elt_path)
        else:
            os.remove(elt_path)

    source_content = os.listdir(source)
    for elt in source_content:
        elt_path = os.path.join(source, elt)
        new_target = os.path.join(target, elt)
        if os.path.isdir(elt_path):
            os.mkdir(new_target)
            copyDir(elt_path, new_target)
        elif os.path.isfile(elt_path):
            shutil.copy(elt_path, target)
            




if __name__ == "__main__":
    main()
