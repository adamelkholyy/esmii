import subprocess
import os
import pandas as pd

model = "deepseek-32b"

# run chadwick analysis (not default esmii prompts)
chadwick_analysis = True
if chadwick_analysis:
	files = [f for f in os.listdir("sections") if f.endswith(".txt")]
	for file in files:

		with open(f"sections/{file}", "r", encoding="utf-8") as f:
			content = f.read()

		prompt = f"""
		Below is a section from an 1842 governmental report investigating the spread of diseases among the labouring class in Britain entitled 
		Report on the Sanitary Condition of the Labouring Population of Great Britain by Edwin Chadwick. The section is titled '{file[:-4]}' and is provided below:

		{content}

		Provide a detailed summary of this section of the report.
		"""

		promptfile = f"{file[:-4]}_summary.txt"
		with open(promptfile, "w", encoding="utf-8") as f:
			f.write(prompt)

		subprocess.run(f'python llm_analysis.py -f "{promptfile}"  -m {model}', shell=True)
		os.remove(promptfile)
	exit()

# filter dataframe for specific participants
df = pd.read_csv("metadata.csv", encoding="cp1252")
df = df[df["Diagnosis"].str.contains("PTSD", na=False)]
participants = df["Participant number"].tolist()

# get filtered transcript paths
filtering = True
transcripts = {"Mother": [], "Staff": [], "SSS": []}
for root, dirs, files in os.walk("transcripts"):
	category = os.path.basename(root)
	for file in files:
		if not filtering or file[:-4] in participants:
			filepath = os.path.join(category, file)
			transcripts[category].append(filepath)

# run analysis
files = transcripts["Mother"] + transcripts["Staff"] + transcripts["SSS"]
for file in files:
	subprocess.run(f'python esmii_analysis.py -f {file} -m {model}', shell=True)
	
