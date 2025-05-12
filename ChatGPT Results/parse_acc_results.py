import csv
import evaluate

generated_text = []
copyrighted = []
count = 0

# Change file name as needed
with open("CSN Accuracy Metric.txt", "r", encoding="utf-8") as accuracy:
    acc_results = accuracy.read()
    # Split results into each prompt and response
    acc_list = acc_results.split("said")

    prompt_count = 0
    i = 0
    while i < len(acc_list):
        text = acc_list[i]
        # Count of distinct prompts within prompt
        gen_count = text.count("Please generate")

        if gen_count == 1:
            try:
                # Isolate prompt and program from generated text
                prompt = text.split("no example usage:")[1].split("\nChatGPT ")[0]
                next_text = acc_list[i+1]

                next_text = next_text.split("You ")[0].strip("\n")
                generated_text.append([prompt, next_text])
            except Exception as e:
                print(repr(e))
                print(i)
                print(text)
            i += 2
        
        # If multiple prompts were submitted at once
        elif gen_count > 1:
            print(i)
            print(text)
            
            i += 2

        # Not a prompt, go to next text
        else:
            i += 1

generated = []
ground_truth = []
all_bleu_scores = []
# <0.1, 0.1-0.3, 0.3-0.5, 0.5-0.7, 0.7+
percentages = [[], [], [], [], []]

# Read ground truth file
with open("../CodeSearchNet/test.csv", "r", encoding="utf-8") as gt:
    gt_results = csv.reader(gt)
    bleu_metric = evaluate.load("bleu")

    g_index = 0
    index = 0
    next(gt_results) # Skip first line since it's the column names
    for line in gt_results:
        ground_truth.append(line[0])
        generated.append(generated_text[g_index][1])
        g_index += 1

        # Compare prediction (generated result) to reference (ground truth)
        this_bleu = bleu_metric.compute(predictions=[generated[-1]], references=[line[0]])["bleu"]
        all_bleu_scores.append(this_bleu)
        # Separate into BLEU score categories
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

# Print total BLEU score and each percentage category BLEU score
bleu_metric = evaluate.load("bleu")
bleu_score = bleu_metric.compute(predictions=generated, references=ground_truth)
print(bleu_score)
print(bleu_score["bleu"] * 100)
print(f"Total: {len(generated_text)}")
for category in percentages:
    print(len(category))