import os
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.2"
__website__ = "http://lukereynolds.net/"
short = False;


# return the number of letters that match
def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


# build a list of word that match the pattern sent to the function
def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and word not in list]


def find(start, words, seen, target, path):
    list = []
    # for each letter in the starting word
    for i in range(len(start)):
        # add the return value of the build function to the list when sent the pattern of the word (e.g. lead: ".ead", "l.ad", "le.d", "lea.")
        list += build(start[:i] + "." + start[i + 1:], words, seen, list)
    # if the list is empty
    if len(list) == 0:
        return False
    # sort the list into pairs showing the current words closeness to the target word followed by the current word (e.g. the word 'load' and 'gold' have 2 of the same letters so it will be represented by (2, 'load'))
    list = sorted([(same(w, target), w) for w in list], reverse=short)
    # for each pair in the list
    for (match, item) in list:
        # if the current word has at least 2 matching letters
        if match >= len(target) - 1:
            # if the current word amount of matching letter is equal to the length of the target word minus 1
            if match == len(target) - 1:
                # append the corresponding word to the path
                path.append(item)
            return True
        # mark that the word has been looked at
        seen[item] = True
    # not really sure
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
            if start in lines:  # start word must be in the list of words
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
                if target in words:  # target word must be in the list of words
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
lines = (open(fname, 'r').read()).split()  # get start word
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

# create an array and fill it with words from the list with the same length as the starting word
words = []
for line in lines:
    word = line.rstrip()
    if len(word) == len(start):
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

while True:
    temp = input("Would you like the short route? y/n: ").lower();
    if temp == 'y':
        short = True;
        break;
    elif temp == 'n':
        break;

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")
