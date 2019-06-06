# regex-dictionary
Search a dictionary of words from the terminal using regular expressions

Requires Python3 and a modern terminal emulator that supports hyperlinks. Each result will link to an online dictionary defining the word unless you set a blank value for the argument `-s`.

Quickly install somewhere on your $PATH (replace `~/.local/bin` with another location on your $PATH if necessary):

    cp dict.py ~/.local/bin/dict
    chmod +x ~/.local/bin/dict
    dict ^hel

By default it uses the word list from `/usr/share/dict/words`, but if you have
another, it can be configured to use something else.

    usage: dict [-h] [-i] [--allow-proper-nouns] [--allow-plurals] [-d DICT]
                [-s SEARCH]
                pattern

    Search a dictionary of words from the terminal using regular expressions.

    positional arguments:
      pattern               A regular expression defining the words you want to
                            match

    optional arguments:
      -h, --help            show this help message and exit
      -i, --case-insensitive
                            Perform a case insensitive search
      --allow-proper-nouns  Include proper nouns (beginnig with capital letter) if
                            any exist in the dictionary
      --allow-plurals       Include words ending in apostrophe-s if any exist in
                            the dictionary
      -d DICT, --dict DICT  Manually specify a file to search
      -s SEARCH, --search SEARCH
                            Online dictionary search format for embedded URLs.
                            Replaces %s in format with matched word. Leave blank
                            to disable embedded URL.

![Sample Terminal Output](/images/screenshot-1.png)
