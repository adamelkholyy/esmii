import subprocess
import os
import pandas as pd



df = pd.read_csv("metadata.csv", encoding="cp1252")
df = df[df["Staff group"] == "Psychiatrist"]
participants = df["Participant number"].tolist()
not_filtering = False

transcripts = {"Mother": [], "Staff": [], "SSS": []}

for root, dirs, files in os.walk("transcripts"):
	category = os.path.basename(root)
	for file in files:
		if file[:-4] in participants or not_filtering:
			filepath = os.path.join(category, file)
			transcripts[category].append(filepath)


# model = "deepseek-7b"
# model = "deepseek-r1:70b"
# model = "deepseek-r1:671b"

model = "deepseek-14b"
model = "deepseek-32b"

print(transcripts)

# files = transcripts["Mother"][:1]
# files = ["Mother/KC-HM12.txt"]
files = transcripts["Staff"]

for file in files:
	subprocess.run(f'python call_deepseek.py -f {file} -m {model}', shell=True)
	
