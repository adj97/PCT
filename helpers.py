from subprocess import Popen, PIPE, call

output_types = {
    "o": " output",
    "e": "  error",
    "h": "   help"
}


def output(type, output):
    output = ["pct", output_types[type], str(output)]
    print(": ".join(output))
