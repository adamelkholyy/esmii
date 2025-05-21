import subprocess
import os


transcripts = {"Mother": [], "Staff": [], "SSS": []}

for root, dirs, files in os.walk("transcripts"):
	category = os.path.basename(root)
	for file in files:
		filepath = os.path.join(category, file)
		transcripts[category].append(filepath)

model = "gpu-deepseek"
model = "largectx-deepseek"

files = transcripts["Mother"][:5]
for file in files:
	subprocess.run(f'python call_deepseek.py -f {file} -m {model}', shell=True)
	
