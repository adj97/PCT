from os import getcwd
from os.path import exists
from json import load

from helpers import (
    output,
    process, 
    checkargs, 
    set_npn, 
    mkba,
    generate_or_update_template,
    rename_dict_key,
    pct_specialise
)

def new(args):

    checkargs(args)

    new_project_name = set_npn(args[0])

    if exists(new_project_name):
        raise Exception("That project already exists")
    elif getcwd().split("\\")[-1]==new_project_name:
        raise Exception("I think you're already in that project folder")

    dj_path = __file__.replace("commands.py","data.json")

    # Boolean for the local data.json being older than the latest push to the template repo
    dj_is_old = False

    if not exists(dj_path) or dj_is_old:
        generate_or_update_template()

    with open(dj_path, "r") as f:
        data = load(f)

    # set project root node name
    data = rename_dict_key(data)

    # Format string templates read from data, but don't overwrite data.json file
    output("o", "Specialising generic pct template")
    data = pct_specialise(data)

    # creating repository structure and writing files
    output("o", "Creating repository structure and writing files")
    process(data, getcwd())

    # create bash alias
    output("o", "Writing bash alias")
    mkba()

    # pct bash alias will open code
    output("o", "Opening vscode in new repository")

    return
