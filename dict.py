#!/usr/bin/env python3

from collections import defaultdict
from urllib.parse import quote
import argparse
import os.path
import shutil
import sys
import re


DEFAULT_DICT = '/usr/share/dict/words'

DEFAULT_ONLINE_DICT = 'https://www.dictionary.com/browse/%s'

BOLD  = "\033[1m"
RED   = "\033[1;31m"
RESET = "\033[0;0m"

SPACE = '  '

url_fmt = '\033]8;;{file}\a{title}\033]8;;\a'

def write_url(stream, text, url):
    stream.write(url_fmt.format(title=text, file=url))


def search_regex(args):
    all_matches = []
    ci_flag = re.IGNORECASE if args.case_insensitive else 0
    with open(args.dict, 'r') as f:
        for line in f:
            trimmed = line.rstrip()
            if len(trimmed) == 0:
                continue
            if not args.allow_proper_nouns and trimmed[0].isupper():
                continue
            if not args.allow_plurals and trimmed.endswith("'s"):
                continue
            matches = list(re.finditer(args.pattern, trimmed, flags=ci_flag))
            if matches:
                formatted = trimmed
                offset = 0
                for match in matches:
                    start, end = match.span()
                    formatted = (
                        formatted[:start+offset] +
                        RED + formatted[start+offset:end+offset] +
                        RESET + formatted[end+offset:]
                    )
                    offset += len(RED) + len(RESET)
                all_matches.append((trimmed, formatted))
    return all_matches


def align_matches(width, all_matches):
    len_matches = len(all_matches)
    num_cols = 1
    max_sizes = defaultdict(int)

    while True:
        new_sizes = defaultdict(int)
        next_col = num_cols + 1
        for idx, (orig, _) in enumerate(all_matches):
            new_sizes[idx % next_col] = max(new_sizes[idx % next_col], len(orig))
        new_sizes[-1] = (next_col - 1) * len(SPACE)  # spacing

        if next_col == len_matches+1 or sum(new_sizes.values()) > width:
            break

        num_cols = next_col
        max_sizes = new_sizes
    return num_cols, max_sizes
            
            

def print_matches(all_matches, col_info, online_dict_fmt):
    num_cols, max_sizes = col_info
    init = True
    for idx, (orig, fmt) in enumerate(all_matches):

        col = idx % num_cols
        col_len = max_sizes[col]
        pad = col_len - len(orig)

        if col != 0:
            sys.stdout.write(SPACE)
        elif not init:
            sys.stdout.write('\n')
        else:
            init = False

        if online_dict_fmt:
            dict_url = online_dict_fmt.replace('%s', orig)
            write_url(sys.stdout, fmt, dict_url)
        else:
            sys.stdout.write(fmt)
        sys.stdout.write(' '*pad)
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a dictionary of words '
                                     'from the terminal using regular expressions.')
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
    parser.add_argument('pattern',
                        help='A regular expression defining the words you want to match')

    args = parser.parse_args()
    terminal_size = shutil.get_terminal_size((80, 20))

    if not os.path.isfile(args.dict):
        print(f"Unable to find dictionary file '{args.dict}'")
        sys.exit(1)

    matches = search_regex(args)

    sys.stdout.write("There were {bold}{num}{reset} matches for "
                     "the string {bold}/{regex}/{reset}\n".format(
        bold=BOLD, reset=RESET, num=len(matches), regex=args.pattern))
    
    col_info = align_matches(terminal_size.columns, matches)
    print_matches(matches, col_info, args.search)
