import subprocess

print("HI!")
import os
print(os.getcwd())

# Run ollama and send "hi!" as input
import subprocess

# Run the command with shell=True so you can use shell input redirection
subprocess.run("ollama run tuned-deepseek-r1:7B < test_prompt.txt", shell=True)


print("Done")
