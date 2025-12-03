import json

with open("tcdv.js", "r") as infile:
    d = json.loads(infile.read())
print(d)
