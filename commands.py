from os import getcwd
from os.path import exists
from json import load

from helpers import (
    output,
    process, 
    checkargs, 
    set_npn, 
    mkba
)

def new(args):

    checkargs(args)

    new_project_name = set_npn(args[0])

    if exists(new_project_name):
        raise Exception("That project already exists")
    elif getcwd().split("\\")[-1]==new_project_name:
        raise Exception("I think you're already in that project folder")

    dj_path = __file__.replace("commands.py","data.json")

    f = open(dj_path)
    data = load(f)

    # recursive function
    output("o", "Creating repository structure")
    process(data["structure"], getcwd())

    # create bash alias
    output("o", "Writing bash alias")
    mkba()

    # bash alias will open code
    output("o", "Opening vscode in new repository")

    return
