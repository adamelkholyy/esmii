import subprocess
import os
import pandas as pd

transcripts = {"Mother": [], "Staff": [], "SSS": []}
model = "deepseek-32b"
filtering = True

# run meta analysis on existing summaries
meta_analysis = True
if meta_analysis:
	subprocess.run(f'python run_meta_analysis.py -f analyses/all_psychiatrists.txt -m {model}', shell=True)
	subprocess.run(f'python run_meta_analysis.py -f analyses/all_ptsd.txt -m {model}', shell=True)
	exit()

# filter dataframe for specific participants
df = pd.read_csv("metadata.csv", encoding="cp1252")
df = df[df["Diagnosis"].str.contains("PTSD", na=False)]
participants = df["Participant number"].tolist()

# get filtered transcript paths
for root, dirs, files in os.walk("transcripts"):
	category = os.path.basename(root)
	for file in files:
		if not filtering or file[:-4] in participants:
			filepath = os.path.join(category, file)
			transcripts[category].append(filepath)

# run analysis
files = transcripts["Mother"] + transcripts["Staff"] + transcripts["SSS"]
for file in files:
	subprocess.run(f'python call_deepseek.py -f {file} -m {model}', shell=True)
	
