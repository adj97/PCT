from os import (
    getcwd, 
    mkdir, 
    walk, 
    chmod, 
    remove, 
    rmdir
)
from os.path import expanduser, join
from stat import S_IWUSR
from inspect import stack
from git import Repo
from random import randint
from json import dumps

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

def process(dictionary, root):
    for key in dictionary:
        filefoldername = "\\".join([root,key])
        contents = dictionary[key]
        if type(contents) == dict:
            mkdir(filefoldername)
            process(contents, filefoldername)
        elif type(contents) == list:
            contents = _pct_specialise(contents)
            with open(filefoldername, "w") as file:
                file.write("\n".join(contents))

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
    template_remote_branch = 'main'

    # Pull template repo
    output("o", "Pulling remote template repo")
    Repo.clone_from(template_remote_url, template_local_path, branch=template_remote_branch)
    _rmtree(template_local_path + "\.git")

    # initial empty data_json
    global data_json
    data_json = {
        "npn_ph": {}
    }

    for root, d_names, f_names in walk(template_local_path):
        # relative root path
        rroot = root.replace(template_local_path,"").replace("\\","")
        
        # set root obj 
        if rroot == "":
            # initial as base location
            rootobj = data_json["npn_ph"]
        else:
            # further loops from previous rootobj
            rootobj = rootobj[rroot]

        # create dirs as empty dict, for further population
        for dn in d_names:
            rootobj[dn] = {}

        # create files as a string array of the file lines
        for fn in f_names:
            fileobj = []
            full_file_path = root + "\\" + fn
            with open(full_file_path, "r") as f:
                for line in f.readlines():
                    fileobj.append(line.replace("\n",""))
            rootobj[fn] = fileobj

    data_json_dump = dumps(data_json, indent=4)

    # write to new datajson file
    dj_path = __file__.replace("helpers.py","data.json")
    # open in "w" mode to overwrite if exists already (old)
    with open(dj_path, "w") as dj_file:
        dj_file.write(data_json_dump)

    # Delete template repo
    _rmtree(template_local_path)

def rename_dict_key(d):
    return {new_project_name if k == "npn_ph" else k:v for k,v in d.items()}

def _pct_specialise(template_lines: list[str]):
    for i,line in enumerate(template_lines):
        template_lines[i] = line.format(new_project_name)
    return template_lines

def dj_is_old():
    # compare existing data.json file created date
    # with the latest push to remote repo
    djisold = False
    return djisold