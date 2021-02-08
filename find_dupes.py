#!/usr/bin/env python

import json
import re
import urllib.request
import editdistance

with urllib.request.urlopen("https://api.vaccinateca.com/v1/locations.json") as response:
    db = json.load(response)

print(f'loaded {len(db["content"])} locations')

content = db["content"]
total_dupes = 0
checked = set()
for i, loc in enumerate(content):
    if i == len(content):
        break
    if i in checked:
        continue
    address = loc.get("Address")
    if address is None:
        continue
    name = loc["Name"]
    dupes = []
    for j, l in enumerate(content[i+1:]):
        address2 = l.get("Address", "")
        if editdistance.eval(address, address2) < 5:
            num1 = address.split()[0]
            num2 = address2.split()[0]
            num1 = int(re.sub("[^0-9]", "", num1))
            num2 = int(re.sub("[^0-9]", "", num2))
            if abs(num1 - num2) < 50:
                dupes.append(address2)
                checked.add(j)

    if len(dupes) > 0:
        print(f"Found duplicates entries for {name}:")
        print("  ", address)
        for a in dupes:
            print("  ", a)
        print()
        total_dupes +=1

print(f"Found {total_dupes} dupes")
