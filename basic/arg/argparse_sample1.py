#!/usr/bin/env python3

# https://docs.python.org/ja/3/howto/argparse.html

"""
# Example
$ ./argparse_sample1.py -h
usage: argparse_sample1.py [-h] [--retry RETRY] [-v] action

positional arguments:
  action         action

options:
  -h, --help     show this help message and exit
  --retry RETRY  max retry
  -v, --verbose  output verbosity

$ ./argparse_sample1.py test -v
test
verbosity turned on
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("action", help="action", type=str)
parser.add_argument("--retry", help="max retry", type=int)
parser.add_argument("-v", "--verbose", help="output verbosity", action="store_true")

args = parser.parse_args()

print(args.action)

if args.verbose:
    print("verbosity turned on")
