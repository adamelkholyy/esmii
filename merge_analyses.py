import os

os.chdir("c:/Users/ae553/Documents/ESMI-II/hpc analyses/")

# read LLM response file and separate final answer
def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(filepath).replace("-deepseek-32b.txt", "")
    content = content.split("</think>")[1]
    content = content.split("\n")[:-3]
    content = filename + "\n" + "\n".join(content)

    return content

# merge multiple LLM responses into one single prompt file
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

if __name__ == "__main__":
    merge_analyses("psychiatrists")
