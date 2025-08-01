import os
import shutil
from enum_types import TextType
from htmlnode import HTMLNode, LeafNode, TextNode
def main():
    working_dir = os.getcwd()
    public_dir = os.path.join(working_dir, "public/")
    static_dir = os.path.join(working_dir, "static/")
    initDirectories(public_dir, static_dir)
    copyDir(static_dir, public_dir)

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
        print(elt)
        elt_path = os.path.join(source, elt)
        new_target = os.path.join(target, elt)
        if os.path.isdir(elt_path):
            print(f"{elt} est un dossier")
            os.mkdir(new_target)
            print(f"{new_target} créé")
            copyDir(elt_path, new_target)
        elif os.path.isfile(elt_path):
            print(f"{elt} est un fichier")
            shutil.copy(elt_path, target)
            print(f"{elt} copié vers {target}")
            




if __name__ == "__main__":
    main()
