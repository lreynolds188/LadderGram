# attempting to decipher... err
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.1"
__website__ = "http://lukereynolds.net/"

def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])

def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and
            word not in list]

def find(word, words, seen, target, path):
    list = []
    for i in range(len(word)):
        list += build(word[:i] + "." + word[i + 1:], words, seen, list)
    if len(list) == 0:
        return False
    list = sorted([(same(w, target), w) for w in list])
    for (match, item) in list:
        if match >= len(target) - 1:
            if match == len(target) - 1:
                path.append(item)
            return True
        seen[item] = True
    for (match, item) in list:
        path.append(item)
        if find(item, words, seen, target, path):
            return True
        path.pop()


# get file name and open corresponding dictionary
fname = input("Enter dictionary name: ")
file = open(fname)
lines = file.readlines()

# while game is running
while True:
    start = input("Enter start word:")  # ask the user for a starting word
    words = []
    for line in lines:
        word = line.rstrip()
        if len(word) == len(start):  # create dictionary containing words of the same length as starting word
            words.append(word)
    target = input("Enter target word:")  # ask the user for the target word
    break

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")
