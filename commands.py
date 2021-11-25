from helpers import *
from cli import *

from os import mkdir
from json import load, dumps


def new(args):
    global new_project_name
    new_project_name = args[0]

    f = open("data.json")
    data = load(f)
    process(data["structure"])

    return


def process(node, root=None):
    print("node: " + str(node))
    for obj in node:
        print("obj: " + str(obj))
        if type(obj["content"]) == list:
            folder_name = obj["name"].format(new_project_name)
            mkdir(folder_name)
            process(obj["content"], folder_name)
        elif type(obj["content"] == str):
            f = open(root + obj["name"], "x")
            f.write(obj["content"].format(new_project_name))
