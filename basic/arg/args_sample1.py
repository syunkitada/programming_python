#!/usr/bin/env python3

"""
# Example
$ ./args.py hoge 100
sys.argv         :  ['./args.py', 'hoge', '100']
type(sys.argv)   :  <class 'list'>
len(sys.argv)    :  3
sys.argv[0]      :  ./args.py
sys.argv[1]      :  hoge
sys.argv[2]      :  100
type(sys.argv[0]):  <class 'str'>
type(sys.argv[1]):  <class 'str'>
type(sys.argv[2]):  <class 'str'>
"""

import sys

print("sys.argv         : ", sys.argv)
print("type(sys.argv)   : ", type(sys.argv))
print("len(sys.argv)    : ", len(sys.argv))

print("sys.argv[0]      : ", sys.argv[0])
print("sys.argv[1]      : ", sys.argv[1])
print("sys.argv[2]      : ", sys.argv[2])
print("type(sys.argv[0]): ", type(sys.argv[0]))
print("type(sys.argv[1]): ", type(sys.argv[1]))
print("type(sys.argv[2]): ", type(sys.argv[2]))
