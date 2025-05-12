"""
Generates 2 text files with desired portion of csv file.
Delimited by \n,\n characters.
"""

import csv

max_funcs = 300
correct_funcs = []
func_descrips = []

with open("CodeSearchNet.csv", "r", encoding="utf-8") as data_file:
    data_reader = csv.reader(data_file)

    index = 0
    for line in data_reader:
        # Do not read more than max_funcs functions
        if index == 0:
            index += 1
            continue
        if index >= max_funcs:
            break
        
        correct_funcs.append(line[0])
        func_descrips.append(line[1])
        index += 1

# Use antidisestablishmentarianism as delimiter for text file
with open("correct_functions.txt", "w", encoding="utf-8") as gt_file:
    for func in correct_funcs:
        gt_file.write(func + " antidisestablishmentarianism\n")

with open("function_descriptions.txt", "w", encoding="utf-8") as inp_file:
    for descrip in func_descrips:
        inp_file.write(descrip + " antidisestablishmentarianism\n")