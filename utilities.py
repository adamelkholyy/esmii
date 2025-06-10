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


def merge_ptsd_analyses():
    answer_files = sorted([f for f in os.listdir("ptsd answers") if f.endswith(".txt")])
    question_files = sorted([f for f in os.listdir("ptsd questions") if f.endswith(".txt")])

    files = list(zip(question_files, answer_files))
    print(files)

    merged_analysis = "# DeepSeek PTSD Interview Analysis: KC-OM4 \n Model: deepseek-32b \n \n Time taken: 6 minutes 43 seconds"
    j = 1
    for question, answer in files:
        with open(f"ptsd questions/{question}", "r", encoding="utf-8") as f:
            q = f.read()

        q_content = q.split("Answer the following questions given the information in the transcript, providing key quotes to support your answer:")[1]
        i = 1
        q_c = "\n **Questions:**"
        for q in q_content.split("\n"):
            if q:
                q_c += "\n" + f"{i}. {q}"
                i += 1
        q_content = q_c

        
        a_content = read_file(f"ptsd answers/{answer}")

        title = a_content.split("\n")[0][2:][:-11].title()
        a_content = "\n".join(a_content.split("\n")[1:])
        print(title)


        merged_analysis += "\n\n" + f"## Theme {j}: " + title + q_content + "\n --- \n **Answers:**  \n" + a_content + "---"
        j += 1

    print(merged_analysis)
    with open("merged_analysis.md", "w", encoding="utf-8") as f:
        f.write(merged_analysis)

if __name__ == "__main__":
    merge_ptsd_analyses()