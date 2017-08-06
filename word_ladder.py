import os
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.8"
__website__ = "http://lukereynolds.net/"


# Function returns the number of letters for each item that match that target word
def same(item, target):
    return len([c for (c, t) in zip(item, target) if c == t])


# Function builds a list of word that match the pattern sent to the function
def build(pattern, words, seen, list):
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and word not in list]


# Function recursively iterates over the each word, gradually moving closer to the target.
def find(start, words, seen, target, path):
    setword = []
    list = []
    # If any letters of the start and target match
    if same(start, target) > 0:
        for i in range(len(start)):
            # Check if new start value is within 1 character of target
            if path[-1][i] == target[i]:
                setword.append(i)
    # for each word
    for i in range(len(start)):
        # if not a word containing target letters
        if i not in setword:
            # add the return value of the build function to the list when sent the pattern of the word
            # (e.g. lead: ".ead", "l.ad", "le.d", "lea.")
            list += build(start[:i] + "." + start[i + 1:], words, seen, list)
    # if the list is empty
    if len(list) == 0:
        return False
    # sort the list into pairs showing the current words closeness to the target word followed by the
    # current word (e.g. the word 'load' and 'gold' have 2 of the same letters so it will be represented by (2, 'load'))
    list = sorted([(same(w, target), w) for w in list], reverse=short)
    # for each pair in the list
    for (match, item) in list:
        # if the current word matches or 1 letter off
        if match >= len(target) - 1:
            # if the current word amount of matching letter is equal to the length of the target word minus 1
            if match == len(target) - 1:
                # append the corresponding word to the path
                path.append(item)
            return True
        # mark that the word has been looked at
        seen[item] = True
    # Set the word to reiterate down the loop.  Start becomes new item
    for (match, item) in list:
        path.append(item)
        if find(item, words, seen, target, path):
            return True
        path.pop()


# Function validates input file
def valid_file(fname):
    try:
        if os.stat(fname).st_size > 0:  # if filename contains data
            return 0
        else:
            return 1
    except OSError:  # if no file of that name found
        return 2


# Function validates input for start word
def valid_start(start, lines):
    if start.isalpha():  # start word must be alphabetic
        if len(start) > 1:  # start word must be larger than 1 character
            if start in lines:  # start word must be in the list of words
                return 0
            else:
                return 3
        else:
            return 4
    else:
        return 5


# Function validates input for target word
def valid_target(start, target, words):
    if target.isalpha():  # target word must be alphabetic
        if len(start) == len(target):  # target word must be same size as start word
            if start != target:  # target and start words must be different
                if target in words:  # target word must be in the list of words
                    return 0
                else:
                    return 6
            else:
                return 7
        else:
            return 8
    else:
        return 9


# Function validates any input y/n
def valid_yn(flag):
    yes_or_no = ['y', 'n']
    if len(flag) == 1:
        if flag.isalpha():
            if flag in yes_or_no:
                if flag == 'y':
                    return 'y'
                else:
                    return 'n'
            else:
                return 10
        else:
            return 11
    elif len(flag) > 1:
        return 12
    else:
        return 13


def print_errormessage(error):
    if error == 1:
        print("Selected file is empty....please reenter")
    elif error == 2:
        print("Can not find the file....please reenter")
    elif error == 3:
        print("Start word not in list of words....please reenter")
    elif error == 4:
        print("Start word must contain more than one letter....please reenter")
    elif error == 5:
        print("Start word must contain only letters....please reenter")
    elif error == 6:
        print("Target word not in list of words....please reenter")
    elif error == 7:
        print("Target word must be different from Start word....please reenter")
    elif error == 8:
        print("Target word must be same length as Start word....please reenter")
    elif error == 9:
        print("Target word must only contain letters....please renter")
    elif error == 10:
        print("Please enter Y or N only")
    elif error == 11:
        print("Please enter letters Y or N only")
    elif error == 12:
        print("Please enter only one character")
    elif error == 13:
        print("Please enter a character")
    return


# Get input dictionary
while True:
    fname = (input("Enter dictionary name: ").lower()).strip()
    file_error = valid_file(fname)
    if file_error == 0:
        # open and read file
        lines = (open(fname, 'r').read()).split()
        break
    else:
        print_errormessage(file_error)

# Get excluded words
while True:
    flag = (input("Would you like to supply a list of words not to use? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    excluded = []
    if yn_error == 'y':
        while True:
            fname = (input("Enter name of file containing characters not to be used: ").lower()).strip()
            file_error = valid_file(fname)
            if file_error == 0:
                # open and read file
                excluded = (open(fname, 'r').read()).split()
                break
            else:
                print_errormessage(file_error)
        break
    elif yn_error == 'n':
        break
    else:
        print_errormessage(yn_error)

# Get start word
while True:
    start = (input("Enter start word: ").lower()).strip()
    start_error = valid_start(start, lines)
    if start_error == 0:
        break
    else:
        print_errormessage(start_error)

# Create an array and fill it with words from the list with the same length as the starting word
# excluded will be blank if the user has decided not to supply any words to omit
words = []
for line in lines:
    word = line.rstrip()
    if len(word) == len(start):
        # If the start word is in the excluded list, do not exclude it
        if (word == start) or (word not in excluded):
            words.append(word)

# Get target word
while True:
    target = (input("Enter target word: ").lower()).strip()
    target_error = valid_target(start, target, words)
    if target_error == 0:
        break
    else:
        print_errormessage(target_error)

# Get shortest or longest path
short = False
while True:
    flag = (input("Would you like the short route? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    if yn_error == 'y':
        short = True
        break
    elif yn_error == 'n':
        break
    else:
        print_errormessage(yn_error)

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")