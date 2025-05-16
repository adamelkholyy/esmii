import subprocess
import time 
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Name of target transcript file")
args = parser.parse_args()

path = os.path.join("transcripts", args.file)
with open(path, "r", encoding="utf-8") as f:
	content = f.read()

mother_prompt = f"""
Conduct a qualitative analysis on the following interview transcript:

{content}

Identify the following from the transcript and provide a written explanation of your findings:

1. The themes from the interview session
2. The treatment/intervention/support received by the interviewee
3. The quality of service received by the interviewee
4. The relationship of the interviewee to their significant sources of support
5. Key quotes from the transcript relevant to the above criteria"""


staff_prompt = f"""
Conduct a qualitative analysis on the following interview transcript:

{content}

Identify the following from the transcript and provide a written explanation of your>

1. The themes from the interview session
2. The treatment/intervention/support offered by the interviewee
3. The quality of service offered by the interviewee
4. The relationship of the interviewee to their patients
5. The job satisfaction of the interviewee
6. Key quotes from the transcript relevant to the above criteria"""


sss_prompt = f"""
Conduct a qualitative analysis on the following interview transcript:

{content}

Identify the following from the transcript and provide a written explanation of your>

1. The themes from the interview session
2. The treatment/intervention/support received by the interviewee's partner/friend/relative etc.
3. The quality of service received by the interviewee's partner/friend/relative etc.
4. The relationship of the interviewee to their partner/friend/relative etc.
5. Key quotes from the transcript relevant to the above criteria"""


print(f"Analysing {args.file}...")
start = time.time()

if "Mother" in args.file:
	prompt = mother_prompt
elif "Staff" in args.file:
	prompt = staff_prompt
elif "SSS" in args.file:
	prompt = sss_prompt
else:
	print(f"Invalid path: {args.file}")
	exit()

subprocess.run(f"ollama run tuned-deepseek-r1:7b '''{prompt}'''" >> analyses/{args.file}, shell=True)
print(f"Completed in {time.time() - start:.2f} seconds")
