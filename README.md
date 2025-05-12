# LLM-Formative

Welcome to LLM-Formative! Feel free to view the completed website at https://sites.google.com/view/llm-formative/home.
In addition, the final report and PDF version of the survey (instead of the original form to avoid exposing responses) for this project is provided for more detailed information.
This project is divided into several folders, where each folder is designed to run separately from the rest.
- The Copilot and ChatGPT Results folders contain the LLM results in the form of a text file as well as Python scripts to analyze them.
- The CodeSearchNet and MBPP folders contain the dataset pulled from their respective papers, a Python script to convert them into text files, and an AutoHotkey script to feed the prompts into the LLM. Note that the script as currently written is designed to begin by pressing the ` button and exit by pressing the esc button. If your machine doesn't have these buttons, feel free to alter it.
- The Manual Datasets folder simply contains the text files that I wrote for certain metrics and an AutoHotkey script to feed them into an LLM. To expand these datasets, simply type a new prompt followed by the delimiter, for which I chose "antidisestablishmentarianism".
- The Website folder contains the three HTML files that compose LLM-Formative's website and a prototype file that I did not fully implement. Since the results are hard-coded into the HTML files, you must alter the HTML files accordingly if you have new results.

# Replication

The Python scripts were executed with Python 3.8.10 and the only additional module is evaluate, which was version 0.4.3.  
The AutoHotkey scripts were executed with AutoHotkey v2. **They will not work correctly if you use AutoHotkey v1.**  
The HTML scripts should function in any browser but were tested in Microsoft Edge.  
However, there are slight differences once embedded in Google Sites, including all hyperlinks opening a new tab: https://support.google.com/sites/thread/147825188/how-do-i-prevent-links-in-my-custom-html-embedded-code-from-opening-a-new-tab.
