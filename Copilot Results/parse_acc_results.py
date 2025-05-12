import csv
import evaluate

generated_text = []
copyrighted = []
count = 0

# Change file name as needed
with open("Accuracy Metric.txt", "r", encoding="utf-8") as accuracy:
    acc_results = accuracy.read()
    # Split results into each prompt and response
    acc_list = acc_results.split("said")
    # print(acc_list[29])

    prompt_count = 0
    i = 0
    while i < len(acc_list):
        text = acc_list[i]
        # Count of distinct prompts within prompt
        gen_count = text.count("Please generate")

        if gen_count == 1:
            prompt = text.split("following: ")[1].split("\nCopilot ")[0]
            next_text = acc_list[i+1]
            # Check that there is a code block in the results
            if next_text.count("python\n\nCopy\n") == 1:
                # Clean extraneous text and spaces from code
                next_text = next_text.split("python\n\nCopy\n")[1]
                next_text = next_text.split("\n\n# Example usage")[0]
                generated_text.append([prompt, next_text])
            
            # Model detected copyrighted material instead
            elif next_text.count("copyright") >= 1:
                copyrighted.append([prompt, next_text])
                generated_text.append([prompt, next_text])
            i += 2

        # If multiple prompts were submitted at once
        elif gen_count > 1:
            prompts = text.split("Please generate a Python function that does the following: \n")[1:]
            prompts[-1] = prompts[-1].split("\nCopilot")[0]
            next_text = acc_list[i+1]
            
            if "1. " in next_text:
                list_nums = [f"{j+1}. " for j in range(gen_count)]
                for j in range(gen_count):
                    split_next_text = next_text.split(list_nums[j])[1]
                    # Separate multiple results in generation if not last
                    if j+1 < gen_count:
                        split_next_text = split_next_text.split(list_nums[j+1])[0]
                    
                    # Go through each item and classify into code or copyright
                    try:
                        split_next_text = split_next_text.split("python\n\nCopy\n")[1]
                        split_next_text = split_next_text.split("\n\n# Example usage")[0]
                        generated_text.append([prompts[j], split_next_text])
                    except:
                        if "copyright" in split_next_text:
                            copyrighted.append([prompts[j], split_next_text])
            elif "copyright" in next_text:
                for j in range(gen_count):
                    copyrighted.append([prompts[j], next_text])
            
            i += 2

        # Not a prompt, go to next text
        else:
            i += 1

generated = []
ground_truth = []
all_bleu_scores = []
# <0.1, 0.1-0.3, 0.3-0.5, 0.5-0.7, 0.7+
percentages = [[], [], [], [], []]

with open("../test.csv", "r", encoding="utf-8") as gt:
    gt_results = csv.reader(gt)
    bleu_metric = evaluate.load("bleu")

    g_index = 0
    index = 0
    for line in gt_results:
        # Copilot does a better job of exactly matching original prompt than ChatGPT
        if line[1] == generated_text[g_index][0].strip("\n "):
            ground_truth.append(line[0])
            generated.append(generated_text[g_index][1])
            g_index += 1

            # Compare generated and ground truth, separate into BLEU score categories
            this_bleu = bleu_metric.compute(predictions=[generated[-1]], references=[line[0]])["bleu"]
            all_bleu_scores.append(this_bleu)
            if this_bleu < 0.1:
                percentages[0].append(this_bleu)
            elif this_bleu < 0.3:
                percentages[1].append(this_bleu)
            elif this_bleu < 0.5:
                percentages[2].append(this_bleu)
            elif this_bleu < 0.7:
                percentages[3].append(this_bleu)
            else:
                percentages[4].append(this_bleu)
        index += 1
        if index > 300 or g_index >= len(generated_text):
            break

# Print results
bleu_metric = evaluate.load("bleu")
bleu_score = bleu_metric.compute(predictions=generated, references=ground_truth)
print(bleu_score)
print(bleu_score["bleu"] * 100)
for category in percentages:
    print(len(category))