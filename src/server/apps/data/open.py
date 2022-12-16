import json

with open("storage1.json", "r") as f:
    d = json.load(f)

    print(d.keys())