import os 
import argparse
from utilities import call_llm

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Transcript filename")
parser.add_argument("-m", "--model", help="Name of LLM to use for analysis ('ollama show' to see available models)", default="deepseek-32b")
parser.add_argument("-d", "--dir", help="Results output directory", default="ptsd_answers")
args = parser.parse_args()


# create a folder for the participant
filename = os.path.basename(args.file[:-4])
outdir = os.path.join(args.dir, filename)
os.mkdir(outdir)

transcript_path = os.path.join("transcripts", args.file)
with open(transcript_path, "r", encoding="utf-8") as f:
    transcript = f.read()

# collate all answers into one folder
question_files = [f for f in os.listdir("ptsd questions") if f.endswith(".txt")]
for file in question_files:
    with open(os.path.join("ptsd_questions", file), "r", encoding="utf-8") as f:
        question = f.read()

    prompt = question.replace("[CONTENTHERE]", transcript)
    promptfile = f"{file[:-4]}-answer.txt"

    with open(promptfile, "w", encoding="utf-8") as temp:
        temp.write(prompt)

    call_llm(promptfile, outdir=outdir, model=args.model)
    os.remove(promptfile)
exit()
