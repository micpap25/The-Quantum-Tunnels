#!/usr/bin/python3

# Load the mapping of states to outputs (constant)
import json, gzip
outputData = json.loads(gzip.GzipFile("outputs.json.gz", 'r').read().decode("utf-8"))

# Dump all the screens
with open("out.txt", "w", encoding="utf-8") as f:
    for key in outputData:
        f.write(outputData[key])
