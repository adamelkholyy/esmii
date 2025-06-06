import subprocess
import time
import os

MODEL = "deepseek-32b"

# call LLM to run analysis given prompt file, output directory, and model name
def call_llm(prompt_file, outdir, model=MODEL):
    outpath =  os.path.join(outdir, os.path.basename(prompt_file))
    print(f"Analysing {prompt_file} using {model}...")
    start = time.time()
    subprocess.run(f"ollama run {model} < '{prompt_file}' >> '{outpath}'", shell=True)
    complete_time = time.time() - start

    with open(outpath, "a", encoding="utf-8") as f:
        f.write(
            "\n"
            + f"Model: {model}"
            + "\n"
            + f"Time taken: {complete_time:.2f} seconds"
            + "\n"
        )

    print(f"Completed in {complete_time:.2f} seconds")


# read LLM response file and separate out final answer
def read_file(filepath, model=MODEL):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(filepath).replace(f"-{model}.txt", "")
    content = content.split("</think>")[1]
    content = content.split("\n")[:-3]
    content = filename + "\n" + "\n".join(content)
    return content


# merge multiple LLM answers into one single file
def merge_analyses(foldername):
    all_content = []
    for root, dirs, files in os.walk(foldername):
        print(root, dirs, files)
        for file in files:
            content = read_file(os.path.join(foldername, file))
            all_content.append(content)

    all_content = "\n".join(all_content)

    with open(f"all_{foldername}.txt", "w", encoding="utf-8") as f:
        f.write(all_content)
