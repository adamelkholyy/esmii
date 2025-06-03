import subprocess
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", help="Name of LLM to prompt")
parser.add_argument("-f", "--file", help="Path to prompt file")
args = parser.parse_args()

outpath =  f"summaries/{os.path.basename(args.file)}"

start = time.time()
print(f"Analysing {args.file}...")
subprocess.run(f"ollama run {args.model} < '{args.file}' >> '{outpath}'", shell=True)
complete_time = time.time() - start

with open(outpath, "a", encoding="utf-8") as f:
    f.write(
        "\n"
        + f"Model: {args.model}"
        + "\n"
        + f"Time taken: {complete_time:.2f} seconds"
        + "\n"
    )

print(f"Completed in {complete_time:.2f} seconds")
