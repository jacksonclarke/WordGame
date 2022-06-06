import os

words = []
easy = []
medium = []
hard = []
extreme = []
cheatList = []

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, "wordstext.txt"), "r") as f:
    for line in f:
        words.append(line.strip())

with open(os.path.join(__location__, "easy.txt"), "r") as f:
    for line in f:
        for word in line.split():
            easy.append(word)

with open(os.path.join(__location__, "medium.txt"), "r") as f:
    for line in f:
        for word in line.split():
            medium.append(word)

with open(os.path.join(__location__, "hard.txt"), "r") as f:
    for line in f:
        for word in line.split():
            hard.append(word)
with open(os.path.join(__location__, "extreme.txt"), "r") as f:
    for line in f:
        for word in line.split():
            extreme.append(word)
with open(os.path.join(__location__, "cheat.txt"), "r") as f:
    for line in f:
        for word in line.split():
            cheatList.append(word)
