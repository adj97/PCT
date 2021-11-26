def help():
    print_message = [
        "Welcome to pct, a cli tool for generating and managing python cli tool code",
        "Commands include: " + ", ".join(commands),
        "usage: pct <command> [parameters]"
    ]
    print('\n'.join(print_message))


commands = [
    "help",
    "new"
]
