from helpers import *
from cli import *

from os import mkdir, getcwd
from json import load


def new(args):
    global new_project_name
    new_project_name = args[0]

    f = open("data.json")
    data = load(f)

    # recursive function
    process(data["structure"], getcwd())

    return


def process(node, root):
    for obj in node:
        if type(obj["content"][0]) == dict:
            folder_name = "/".join([root, obj["name"].format(new_project_name)])
            mkdir(folder_name)
            process(obj["content"], folder_name)
        elif type(obj["content"][0] == str):
            file_name = "/".join([root, obj["name"]])
            f = open(file_name, "x")
            f.write("\n".join(obj["content"]).format(new_project_name))
