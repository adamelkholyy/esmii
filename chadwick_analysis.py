import os
from utilities import call_llm

# run chadwick question analysis
chadwick_questions = True
if chadwick_questions:
	files = [f for f in os.listdir("questions") if f.endswith(".txt")]

	with open("chadwick.txt", "r", encoding="utf-8") as f:
		chadwick_document = f.read()

	for file in files:
		with open(f"questions/{file}", "r", encoding="utf-8") as f:
			content = f.read()
		prompt = content.replace("[CONTENTHERE]", chadwick_document)

		promptfile = f"{file[:-4]} answer.txt"
		with open(promptfile, "w", encoding="utf-8") as f:
			f.write(prompt)

		call_llm(promptfile, outdir="answers")
		os.remove(promptfile)
	exit()


# run chadwick summary analysis
chadwick_summary = False
if chadwick_summary:
	files = [f for f in os.listdir("sections") if f.endswith(".txt")]
	for file in files:

		with open(f"sections/{file}", "r", encoding="utf-8") as f:
			content = f.read()

		prompt = f"""
		Below is a section from an 1842 governmental report investigating the spread of diseases among the labouring class in Britain entitled 
		Report on the Sanitary Condition of the Labouring Population of Great Britain by Edwin Chadwick. The section is titled '{file[:-4]}' and is provided below:

		{content}

		Provide a detailed summary of this section of the report.
		"""

		promptfile = f"{file[:-4]} summary.txt"
		with open(promptfile, "w", encoding="utf-8") as f:
			f.write(prompt)

		call_llm(promptfile, outdir="summaries")
		os.remove(promptfile)
	exit()
