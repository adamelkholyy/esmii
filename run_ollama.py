import subprocess
import time 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Name of target transcript file")
args = parser.parse_args()

with open(args.file, "r", encoding="utf-8") as f:
	content = f.read()

prompt = f"""
Conduct a qualitative analysis on the following interview transcript:

{content}

Identify the following from the transcript and provide a written explanation of your findings:

1. The themes from the interview session
2. The treatment/intervention/support received by the interviewee
3. The quality of service received by the interviewee
4. The relationship of the interviewee to their significant sources of support
5. Key quotes from the transcript relevant to the above criteria
Put your final answers within \boxed{'{}'}"""

start = time.time()
subprocess.run(f"ollama run tuned-deepseek-r1:7b '''{prompt}''' >> {args.file[:-4]}_analysis_boxed.txt", shell=True)
print(f"Completed in {time.time() - start:.2f} seconds")
