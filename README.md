# Python CLI tool generator
This repo is itself a python cli tool that generates the boilerplate source code files and structure of a generic python cli tool

## Bash Alias
    pct(){
        python /<srcpath>/main.py $@
        code $2
    }

## PyTests
Install: `pip install pytest`

Run: `pytest tests/`