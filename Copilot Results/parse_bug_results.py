generated_text = []
count = 0

# Change file name as needed
with open("MBPP Accuracy Metric.txt", "r", encoding="utf-8") as accuracy:
    acc_results = accuracy.read()
    # Split results into each prompt and response
    acc_list = acc_results.split("said")

    # Clean results
    prompt_count = 0
    i = 0
    while i < len(acc_list):
        text = acc_list[i]
        if " Please only" in text:
            # Isolate prompt from generated text
            prompt = text.split(" Please only")[0].strip("\n")
            next_text = acc_list[i+1]

            # Clean extraneous text and spaces from code
            next_text = next_text.split("python\n\nCopy\n")[1].split("You ")[0].strip("\n")
            generated_text.append([prompt, next_text])
        i += 1

import json

# Sample Columns: [source_file, task_id, prompt, code, test_imports, test_list]
data_file = open("../sanitized-mbpp.json")
data = json.load(data_file)

# Result categories
valid = 0
fail = 0
buggy = 0
bug_types = set()

# Analyze results
g_index = 0
index = 0
for line in data:
    if line["prompt"].strip(" ").replace("python ", "") == generated_text[g_index][0].replace("python ", ""):
        # Ensure generated code and ground truth code have same function name
        generated_code = generated_text[g_index][1]
        llm_sig = generated_code.split("def ")[1].split("(")[0]
        gt_sig = line["code"].split("def ")[1].split("(")[0]
        generated_code = generated_code.replace(llm_sig, gt_sig)

        for test in line["test_list"]:
            generated_code += "\n" + test

        # Run generated code. Passes only if no error
        try:
            exec(generated_code)
            valid += 1
        except AssertionError:
            fail += 1
        except Exception:
            buggy += 1
        # except Exception as ex:
        #     bug_types.add(str(repr(ex)).split("(")[0])

        g_index += 1
    index += 1
    if index > 200 or g_index >= len(generated_text):
        break

# Print results
print(f"Valid: {valid} Fail: {fail} Bug: {buggy}")