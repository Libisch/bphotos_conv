# -*- coding: utf-8 -*-

import json

input_file = open("all_photos_new_array.json", "r")
old_data = json.load(input_file)
new_data = {}   

for i in range(len(old_data)):
    slug = old_data[i]["Slug"]["En"]
    pictureid = old_data[i]["Pictures"][0]
    slug = old_data[i]["Slug"]["En"]
    if slug in new_data:
        new_data[slug]["Pictures"].append(pictureid)
    else:
        new_data[slug] = old_data[i]

all_docs = json.dumps(new_data)
with open('bagnowka_all.json', 'w') as file:
    file.write(all_docs)
print("Done. open 'bagnowka_all.json' to see all Bagnowka photos in sorted by galleries")