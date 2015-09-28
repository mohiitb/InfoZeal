#!/usr/bin/env python

import sys
import json
import cgi

fs = cgi.FieldStorage()
#print fs
print ("Content-Type: application/json")
print ("\n")
print ("\n")


result = {}
result['success'] = True

d = {}
for k in fs.keys():
    d[k] = fs.getvalue(k)

result['data'] = d
filename = "log.txt"
target = open(filename, 'a')
target.write(json.dumps(result,indent=1))
target.write("\n")
target.close()