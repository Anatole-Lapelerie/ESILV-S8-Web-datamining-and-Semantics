file1 = open("gares-tgv_jsonld_to-update.json", "r")
file2 = open("gares-tgv_jsonld.json", "a")

i = 0

for row in file1:
    if '      "Id":' in row:
        i = i + 1
        new_row = '      "Id": "' + str(i) + '",\n'
        file2.write(new_row)
    else:
        file2.write(row)
        
file1.close()
file2.close()