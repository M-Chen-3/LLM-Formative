import json

# Sample Columns: [source_file, task_id, prompt, code, test_imports, test_list]
data_file = open("sanitized-mbpp.json")
data = json.load(data_file)

max_funcs = 200
correct_funcs = []
func_descrips = []

# Data is list of dict, where each dict is a sample
for index, sample in enumerate(data):
    # More intelligent solution for not reading more than max_funcs functions
    if index >= max_funcs:
        break
    correct_funcs.append(sample["code"])
    func_descrips.append(sample["prompt"])

# Use antidisestablishmentarianism as delimiter for text file
with open("correct_functions.txt", "w", encoding="utf-8") as gt_file:
    for func in correct_funcs:
        gt_file.write(func + " antidisestablishmentarianism\n")

with open("function_descriptions.txt", "w", encoding="utf-8") as inp_file:
    for descrip in func_descrips:
        inp_file.write(descrip + " antidisestablishmentarianism\n")