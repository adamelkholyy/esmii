import subprocess
import time
import argparse
import os

# prompts for mother, staff, and SSS interview transcripts

mother_prompt = f"""
Below is a transcript of an interview between a mother and a psychology researcher. 
The aim of the interview was to understand the experiences of mothers who have been through perinatal mental health services. 
You will be asked to answer some questions about the mother's experience, based on the interview transcript below:

{content}

Answer the following questions given the information in the transcript:

1. What were the key mental health problems that brought the mother to the perinatal mental health team? 
2. What was the mother's journey through the healthcare system in getting to the perinatal mental health service? Who referred her and at what stage in the treatment pipeline?
3. What components of care did the mother receive as part of the service? 
4. What was the experience of the mother who received care from the perinatal mental health team? What factors, and care, affected her experience? Which parts of care were positive, which parts were negative? 
5. What role did other branches of the healthcare system have? Did they help/impede the mother's treatment?
6. Did the mother have any dissapointments or report anything lacking in the treatment they recieved?
7. Did the mother demonstrate any conflicting attitudes or contradictions within the interview?
8. Was there any treatment relevant to the mother's diagnosis that was missing or not offered to her?
9. Identify key quotes from the transcript to support your above answers.
"""


staff_prompt = f"""
Below is a transcript of an interview between a perinatal mental health staff member and a psychology researcher.
The aim of the interview was to understand the experiences of perinatal mental health staff members when working with patients.
You will be asked to answer some questions about the mother's experience, based on the transcript below:

{content}

Answer the following questions given the information in the transcript:

1. What was the staff member's attitude toward their patients? Were their patients compliant/adherent to treatment?
2. What treatment does the staff memeber offer to mothers suffering from perinatal mental health issues?
3. What is the staff member's attitude toward their own work? Are they satisfied in their current role?
4. What were the self-reported limitations of the treatment offered by the staff member, if any?
5. What were the self-reported potential improvements to the service offered by the staff member, if any?
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


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Name of target transcript file")
parser.add_argument("-m", "--model", help="Name of LLM to prompt")
parser.add_argument("-d", "--dir", help="Name of directory for analyses to be saved in", default="analyses")
args = parser.parse_args()

print(f"Analysing {args.file} using {args.model}")
start = time.time()

# switch to correct prompt
if "Mother" in args.file:
    prompt = mother_prompt
elif "Staff" in args.file:
    prompt = staff_prompt
elif "SSS" in args.file:
    prompt = sss_prompt
else:
    raise FileNotFoundError(f"Invalid path: {args.file}")

# read transcript file and write prompt out to temp file
inpath = os.path.join("transcripts", args.file)
with open(inpath, "r", encoding="utf-8") as f:
    content = f.read()

with open("prompt.txt", "w", encoding="utf-8") as temp:
    temp.write(prompt)

# call deepseek for analysis
outpath = os.path.join(args.dir, f"{args.file[:-4]}-{args.model}.txt")
subprocess.run(f"ollama run {args.model} < prompt.txt >> {outpath}", shell=True)
complete_time = time.time() - start

# write out deepseek response with model metadata
with open(outpath, "a", encoding="utf-8") as f:
    f.write(
        "\n"
        + f"Model: {args.model}"
        + "\n"
        + f"Time taken: {complete_time:.2f} seconds"
        + "\n"
    )

print(f"Completed in {complete_time:.2f} seconds")
