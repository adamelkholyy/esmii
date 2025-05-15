import subprocess

# HERTS
files = ["KC-HM11",
        "KC-HM12",
        "KC-HM13",
        "KC-HM8",
        "KC-HM9",
        "KC-HM4",
        "KC-HM10",
        "KC-HM14",
        "KC-HM3",
        "KC-HM1",
        "KC-HM2",
        "KC-HM7",
        "KC-HM5",
        "KC-HM6",]

# HERTS
files = ["SSS/KC-HP3", "SSS/KC-HP4", "Staff/KC-HS1", "Staff/KC-HS2"]


for file in files:
        subprocess.run(f'python run_ollama.py -f {file}.txt', shell=True)

