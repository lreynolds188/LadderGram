import os
import re


# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.2"
__website__ = "http://lukereynolds.net/"


def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list):
    return [word for word in words
                 if re.search(pattern, word) and word not in seen.keys() and
                    word not in list]


def find(start, words, seen, target, path):
    list = []
    for i in range(len(start)):
        list += build(start[:i] + "." + start[i + 1:], words, seen, list)
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


# validate file
def valid_file(fname):
    try:
        if os.stat(fname).st_size > 0:  # if filename contains data
            return 0
        else:
            return 1
    except OSError:  # if no file of that name found
            return 2


# validate start word
def valid_start(start, lines):
    if start.isalpha():  # start word must be alphabetic
        if len(start) > 1:  # start word must be larger than 1 character
            if start in lines: # start word must be in the list of words
                return 0
            else:
                return 1
        else:
            return 2
    else:
        return 3


# validate target word
def valid_target(start, target, words):
    if target.isalpha():  # target word must be alphabetic
        if len(start) == len(target):  # target word must be same size as start word
            if start != target:  # target and start words must be different
                if target in words: # target word must be in the list of words
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            return 3
    else:
        return 4


# get file name
while True:
    fname = input("Enter dictionary name: ").lower()
    ferror = valid_file(fname)
    if ferror == 0:
        break
    elif ferror == 1:
        print("Selected file is empty....please reenter")
    else:
        print("Can not find the file....please reenter")


# open corresponding dictionary
lines = (open(fname, 'r').read()).split()
# while game is running
while True:
    # get start word
    while True:
        start = (input("Enter start word: ").lower()).strip()
        serror = valid_start(start, lines)
        if serror == 0:
            break
        elif serror == 1:
            print("Start word not in list of words....please reenter")
        elif serror == 2:
            print("Start word must contain more than one letter....please reenter")
        else:
            print("Start word must contain only letters....please reenter")

    words = []
    for line in lines:
        word = line.rstrip()
        if len(word) == len(start):  # create dictionary containing words of the same length as starting word
            words.append(word)

    # get target word
    while True:
        target = (input("Enter target word: ").lower()).strip()
        terror = valid_target(start, target, words)
        if terror == 0:
            break
        elif terror == 1:
            print("Target word not in list of words....please reenter")
        elif terror == 2:
            print("Target word must be different from Start word....please reenter")
        elif terror == 3:
            print("Target word must be same length as Start word....please reenter")
        else:
            print("Target word must contain only letters....please reenter")

    break

count = 0
path = [start]
seen = {start : True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")