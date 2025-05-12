import csv
import evaluate

generated_text = []
copyrighted = []
count = 0

# Change file name as needed
with open("CSn Consistency Metric.txt", "r", encoding="utf-8") as accuracy:
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

# <0.7, 0.7-0.9, 0.9+
percentages = [[], [], []]
all_bleu_scores = []
bleu_metric = evaluate.load("bleu")

prompt = ""
starwalker = ""

# Analyze results
for line in generated_text:
    # Assign first prompt to be the reference
    if line[0] != prompt:
        prompt = line[0]
        starwalker = line[1]
    # For the 4 identical prompts afterwards, compare to first result
    elif line[0] == prompt:
        this_bleu = bleu_metric.compute(predictions=[starwalker], references=[line[1]])["bleu"]
        all_bleu_scores.append(this_bleu)
        if this_bleu < 0.7:
            percentages[0].append(this_bleu)
        elif this_bleu < 0.9:
            percentages[1].append(this_bleu)
        else:
            percentages[2].append(this_bleu)

# Print results
print(f"Average BLEU Score: {sum(all_bleu_scores) / len(all_bleu_scores)}")
for category in percentages:
    print(len(category))
print(len(generated_text))