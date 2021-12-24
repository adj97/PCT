from os import mkdir
from inspect import stack

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
