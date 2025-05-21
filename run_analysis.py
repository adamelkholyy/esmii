import subprocess
import os


transcripts = {"Mother": [], "Staff": [], "SSS": []}

for root, dirs, files in os.walk("transcripts"):
	category = os.path.basename(root)
	for file in files:
		filepath = os.path.join(category, file)
		transcripts[category].append(filepath)

# model = "deepseek-7b"
model = "deepseek-14b"
model = "deepseek-32b"
# model = "deepseek-r1:70b"
## model = "deepseek-r1:671b" #too expensive

files = transcripts["Mother"][:1]
files = ["Mother/KC-HM12.txt"]

for file in files:
	subprocess.run(f'python call_deepseek.py -f {file} -m {model}', shell=True)
	
