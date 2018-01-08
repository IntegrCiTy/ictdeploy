import sys
import json

with open(sys.argv[1]) as data_file:
    data = json.load(data_file)
print("initial values ->", data)
