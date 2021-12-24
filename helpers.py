from os import (
    getcwd, 
    mkdir, 
    walk, 
    chmod, 
    remove, 
    rmdir,
    listdir
)
from os.path import expanduser, join
from stat import S_IWUSR
from inspect import stack
from git import Repo
from random import randint

output_types = {
    "o": " output",
    "e": "  error",
    "h": "   help"
}

def output(type, output):
    output = ["pct", output_types[type], str(output)]
    print(": ".join(output))

def set_npn(npn):
    global new_project_name
    new_project_name = npn
    return npn

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

def checkargs(args):
    # inspect.stack() returns the full stack trace info
    # stack[1] is the first parent (0 is the current location)
    # parent[3] is the "code" element which is the parent method name
    method = stack()[1][3]

    if method == "new":
        if len(args) != 1:
            raise Exception("The \"new\" command expects a single argument")

def mkba():

    # gather prerequesite strings
    mainpath = "/".join([*getcwd().split("\\"), new_project_name, "main.py"]) # filepath of main.py for the NEW tool
    tilde = expanduser("~/") # make ~ explicit for paths
    pct_strings = [ # bash alias for the created python cli tool
        "# Alias for python cli tool " + new_project_name,
        new_project_name + "(){",
        "    python " + mainpath + " $@",
        "}"
    ]
    sba_strings = [ # bashrc code to source bash_aliases
        "# Separate file for custom bash aliases",
        "if [ -f ~/.bash_aliases ]; then",
        "    . ~/.bash_aliases",
        "fi"
    ]

    pct_alias, source_bash_aliases = compile_alias(pct_strings, sba_strings)

    # read(r) then append(+) bashrc
    with open(tilde + '.bashrc', 'r+') as bashrc:
        if ". ~/.bash_aliases" not in bashrc.read():
            bashrc.write(source_bash_aliases)

    # (create and) write to bash_aliases
    with open(tilde + '.bash_aliases', 'a') as bash_aliases:
        bash_aliases.write(pct_alias)

    return

def compile_alias(*argv):
    stringss = []
    for i,strings in enumerate(argv):
        stringss.append("\n".join(["","",*strings,""]))
    return stringss

def _rmtree(top):
    chmod(top, S_IWUSR)
    for root, dirs, files in walk(top, topdown=False):
        for name in files:
            filename = join(root, name)
            chmod(filename, S_IWUSR)
            remove(filename)
        for name in dirs:
            rmdir(join(root, name))
    rmdir(top)  

def generate_or_update_template():
    # uri's
    template_remote_url = "https://github.com/adj97/PythonCliToolTemplate.git"
    template_local_path = getcwd() + "T_" + str(randint(100000, 999999))

    # Pull template repo
    Repo.clone_from(template_remote_url, template_local_path, branch='main')

    # get folder structure of pulled repo
    file_structure=listdir(template_local_path)
    file_structure.remove('.git')
    for i, filename in enumerate(file_structure):
        if len(filename.split("."))==1:
            file_structure[i]=[filename + "\\" + c for c in listdir(template_local_path + "\\" + filename)]
    print(file_structure)

    # read each file
    for file in file_structure:
        with open(template_local_path + "\\" + file, "r") as f:
            print(f.readline())

    dj_path = __file__.replace("helpers.py","data.json")

    # write to new datajson file
    with open(dj_path, "w") as datajson:
        datajson.write("\n".join([
            "{",
            "    \"structure\": [",
            "    ]",
            "}"
        ]))

    # Delete template repo
    _rmtree(template_local_path)