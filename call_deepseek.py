import subprocess
import time 
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Name of target transcript file")
parser.add_argument("-m", "--model", help="Name of LLM to prompt")
args = parser.parse_args()

path = os.path.join("transcripts", args.file)
with open(path, "r", encoding="utf-8") as f:
	content = f.read()

old_mother_prompt = f"""
Conduct a qualitative analysis on the following interview transcript:

{content}

Identify the following from the transcript and provide a written explanation of your findings:

1. The themes from the interview session
2. The treatment/intervention/support received by the interviewee
3. The quality of service received by the interviewee
4. The relationship of the interviewee to their significant sources of support
5. Key quotes from the transcript relevant to the above criteria"""


mother_prompt = f"""
Below is a transcript of an interview between a mother and a psychology researcher. 
The aim of the interview was to understand the experiences of mothers who have been through perinatal mental health services. 
You will be asked to answer some questions about the mother's experience, based on the interview transcript below:

{content}

Answer the following questions given the information in the transcript:

1. What were the key mental health problems that brought the mother to the perinatal mental health team? 
2. What was the mother's journey to get to the perinatal mental health service? Who referred her?
3. What components of care did the mother receive as part of the service? 
4. What was the experience of the mother who received care from the perinatal mental health team? What factors, and care, affected her experience? Which parts of care were positive, which parts were negative? 
5. What role did other branches of the healthcare system have? Did they help/impede the mother's treatment?
6. Identify key quotes from the transcript to support your above answers.
"""



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

prompt = "Hi!"
with open("prompt.txt", "w", encoding="utf-8") as temp:
	temp.write(prompt)

subprocess.run(f"ollama run {args.model} < prompt.txt >> {os.path.join('analyses', args.file)}", shell=True)

print(f"Completed in {time.time() - start:.2f} seconds")
