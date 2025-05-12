import evaluate

generated_text = []
count = 0

# Change file name as needed
with open("CSN Consistency Metric.txt", "r", encoding="utf-8") as consistency:
    cons_results = consistency.read()
    # Split results into each prompt and response
    cons_list = cons_results.split("said")

    # Clean results
    prompt_count = 0
    i = 0
    while i < len(cons_list):
        text = cons_list[i]
        if "Please generate" in text:
            prompt = text.split("example usage:\n\n")[1].strip("Copilot ")
            next_text = cons_list[i+1]

            # Clean extraneous text and spaces from code
            next_text = next_text.split("python\n\nCopy\n")[1].split("You ")[0].strip("\n")
            generated_text.append([prompt, next_text])
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