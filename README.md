# Python CLI tool generator
This repo is itself a python cli tool that generates the boilerplate source code files and structure of a generic python cli tool

## Bash Alias
    pct(){
        python <src path>/pct/main.py $@
        exitcode=$?
        if [ "${exitcode}" -eq 0 ];
        then
            code $2
        fi
    }

## PyTests
Install: `pip install pytest`

Run: `pytest tests/`