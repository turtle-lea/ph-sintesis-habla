#!/usr/bin/env python

import sys

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

param = sys.argv[1]
entry = "_" + param + "_"
arr = [0, 1, 2, 3, 4, 5]
res = []

for index, item in enumerate(entry[0:len(entry)-1]):
	res.append(entry[index] + entry[index+1])

print res
