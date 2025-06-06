import subprocess
import os
import pandas as pd

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
files = files[0]
for file in files:
	# subprocess.run(f'python base_analysis.py -f {file} -d analyses', shell=True)
	subprocess.run(f'python ptsd_analysis.py -f {file}', shell=True)

