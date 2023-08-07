#!/usr/bin/env python3

import argparse
import random
import sys
import os

import dict as dict_lib


DEFAULT_DICT = '/usr/share/dict/words'

DEFAULT_ONLINE_DICT = 'https://www.dictionary.com/browse/%s'

BOLD  = "\033[1m"
RED   = "\033[1;31m"
RESET = "\033[0;0m"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a dictionary of words '
                                     'from the terminal using regular expressions.')
    parser.add_argument('-n', type=int, default=1,
                        help='Repeat this N times (default = 1)')
    parser.add_argument('-i', '--case-insensitive', action='store_true',
                        help='Perform a case insensitive search')
    parser.add_argument('--allow-proper-nouns', action='store_true',
                        help='Include proper nouns (beginnig with capital '
                             'letter) if any exist in the dictionary')
    parser.add_argument('--allow-plurals', action='store_true',
                        help='Include words ending in apostrophe-s if any '
                             'exist in the dictionary')
    parser.add_argument('-d', '--dict', default=DEFAULT_DICT,
                        help='Manually specify a file to search')
    parser.add_argument('-s', '--search', default=DEFAULT_ONLINE_DICT,
                        help='Online dictionary search format for embedded '
                             'URLs. Replaces %%s in format with matched word. '
                             'Leave blank to disable embedded URL.')
    parser.add_argument('patterns', nargs='+',
                        help='Multiple regular expressions defining the phrase you want to match')

    args = parser.parse_args()
    
    if not os.path.isfile(args.dict):
        print(f"Unable to find dictionary file '{args.dict}'")
        sys.exit(1)

    phrases = []
    for x in range(args.n):
        phrases.append([])

    for pattern in args.patterns:
        args.pattern = pattern
        matches = dict_lib.search_regex(args)

        for p in phrases:
            if not matches:
                p.append(('*', '*'))
            else:
                p.append(random.choice(matches))

    for phrase in phrases:
        for word in phrase:
            print(word[1], end=' ')
        print()

