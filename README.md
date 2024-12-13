# Package Name

## Overview


## Running

To run, in a terminal run

    dict

To see logs, another application has to be started before the application is started. In a terminal run:

    textual console

Then, instead of running the normal apllication, in another terminal run:

    dict-dev -v

To see debug messages, run the application with:

    dict-dev -vvv

Since the amount of logs from textual itself might be too big, some messages could be supressed by running:

    textual console -x EVENT -x SYSTEM

To enable auto complete, run in the terminal the command below, or add the command to the *.bashrc* or *.zshrc* file:

    eval "$(_DICT_COMPLETE=bash_source dict)"
    eval "$(_DICT_COMPLETE=zsh_source dict)"
