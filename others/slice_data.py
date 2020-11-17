
import json
import os

file_name   = 'demo/slash/{}.json'
file_number = 0
file_name_number = file_name.format(file_number)
f = open('demo/slash.json', "r")
f2 = open(file_name_number,"w")
count = 0
for x in f:
    count = count + 1
    print(count)
    print(x)
    data = json.loads(x)
    temp = file_number
    if "key1" in data and data["key1"] == "1":
        file_number = file_number + 1
    if "key2" in data and data["key2"] == "1":
        file_number = file_number + 1
    if file_number > temp:
        f2.close()
        if os.stat(file_name_number).st_size < 500:
            file_number  = file_number - 1
        file_name   = 'demo/slash/{}.json'

        file_name_number = file_name.format(file_number)
        print(file_name_number)
        f2 = open(file_name_number, "w")

    f2.write(x)
    f2.write("\n")
