#!/usr/bin/python

import os
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.16"
__website__ = "http://lukereynolds.net/"


def same(item, target):
    """
    Function returns the number of letters for each item that match that target word.

    :param item: Word being compared to the Target letter by letter
    :type item: str
    :param target: Target Word
    :type target: str
    :return: Integer of the number of letter matches for the word
    :rtype: int
    """
    return len([c for (c, t) in zip(item, target) if c == t])


def build(pattern, words, seen, list):
    """
    Function builds a list of word that match the pattern provided as input.

    :param pattern: Pattern changes on each evocation - e.g. lead: ".ead", "l.ad", "le.d", "lea.")
    :type pattern: str
    :param words: List of all words
    :type words: list
    :param seen: Dictionary with words and a value of true if they have been identified
    :type seen: dict
    :param list: List of words that match the current pattern and are not in seen
    :type list: list
    :return: Words matching pattern
    :rtype: list
    """
    return [word for word in words
            if re.search(pattern, word) and word not in seen.keys() and word not in list]


def find(start, words, seen, target, path):
    """
    Function recursively iterates over the each word, gradually moving closer to the target.

    :param start: Current starting word - changes as this is recursively called
    :type start: str
    :param words: List of words
    :type words: List
    :param seen: List of words current processed - seen
    :type seen: dict
    :param target: Target word
    :type target: str
    :param path: Current path to the target word
    :type path: List
    :return: True if found or False if no path for current item
    :rtype: Boolean
    """
    matchedletters = []
    list = []

    # Determine whether start and target letters match. Exclude matching letters from pattern.
    if (sum(1 for (c, t) in zip(start, target) if c == t)) > 0:
        # Compare the new start word to the target word and return a list containing indexes of matched letters
        matchedletters = [i for i, x in enumerate(zip(start, target)) if all(y == x[0] for y in x)]
    for i in range(len(start)):
        # For each letter position, only build a pattern for letter positions that have not already been found.
        if i not in matchedletters:
            # Add all words matching the pattern to the list. Only process patterns where the letter has not been found
            list += build(start[:i] + "." + start[i + 1:], words, seen, list)

    # If the list is empty (no matching words found) - Exit the iteration and process the next item if one exists.
    if len(list) == 0:
        return False

    # Sort the list by number of matches and alphabetically.  If reverse is specified sort by matched letters first
    list = sorted([(same(w, target), w) for w in list], reverse=short)

    for (match, item) in list:

        # If the current word matches target or 1 letter off target.
        if match >= len(target) - 1:
            if match == len(target) - 1:
                # Append the word to the path and exit the recursion, as we have found the last word.
                path.append(item)
            return True
        # For each word in the current list mark it true so that future word searches exclude the word.
        seen[item] = True

    # Set the first word in the list to be the new start word to iterate on.
    for (match, item) in list:
        # Append the word to the list and start recursively searching.
        path.append(item)
        # Recursively call self.
        if find(item, words, seen, target, path):
            return True
        # Remove the last word in path if could not find a path for this item.
        path.pop()


def valid_file(fname):
    """
    Function to validate input files.

    :param fname: File name input
    :type fname: str
    :return: String indicating whether file data is valid
    :rtype: str
    """
    try:
        if os.stat(fname).st_size > 0:  # if filename contains data
            return "0"
        else:
            return "Selected file is empty....please reenter"
    except OSError:
        return "Can not find the file....please reenter"


def make_word_list(start, lines, excluded):
    """
    Function to build a word file catering for any excluded word.

    :param start: Start word input
    :type start: str
    :param lines: List of dictionary words
    :type lines: list
    :param excluded: List of excluded dictionary words
    :type excluded: list
    :return: Final list of words
    :rtype: list
    """
    words = []
    for line in lines:
        word = line.rstrip()
        if len(word) == len(start):
            if (word == start) or (word not in excluded):
                words.append(word)
    return words

def valid_start(start, lines):
    """
    Function to validate input for start word.

    :param start: Start word input
    :type start: str
    :param lines: List of dictionary words
    :type lines: list
    :return: String indicating whether data is valid
    :rtype: str
    """
    if start.isalpha():  # start word must be alphabetic
        if len(start) > 1:  # start word must be larger than 1 character
            if start in lines:  # start word must be in the list of words
                return "0"
            else:
                return "Start word not in list of words....please reenter"
        else:
            return "Start word must contain more than one letter....please reenter"
    else:
        return "Start word must contain only letters....please reenter"


def valid_target(start, target, words):
    """
    Function to validate input for target word.

    :param start: Start word input
    :type start: str
    :param target: Target word input
    :type target: str
    :param words: List of dictionary words
    :type words: list
    :return: String indicating whether data is valid
    :rtype: str
    """
    if target.isalpha():  # target word must be alphabetic
        if len(start) == len(target):  # target word must be same size as start word
            if start != target:  # target and start words must be different
                if target in words:  # target word must be in the list of words
                    return "0"
                else:
                    return "Target word not in list of words....please reenter"
            else:
                return "Target word must be different from Start word....please reenter"
        else:
            return "Target word must be same length as Start word....please reenter"
    else:
        return "Target word must contain only letters....please reenter"


def valid_yn(flag):
    """
    Function to validate y/n options.

    :param flag: String indicating yes or no
    :type flag: str
    :return: String indicating whether data is valid
    :rtype: str
    """
    yes_or_no = ['y', 'n']
    if len(flag) == 1:  # flag must be one character
        if flag.isalpha():  # flag must be alphabetic
            if flag in yes_or_no:  # target word must be Y or N
                if flag == 'y':
                    return "y"
                else:
                    return "n"
            else:
                return "Please enter Y or N only"
        else:
            return "Please enter letters Y or N only"
    elif len(flag) > 1:
        return "Please enter only one character"
    else:
        return "Please enter a character"


# Get input dictionary file
while True:
    fname = (input("Enter dictionary name: ").lower()).strip()
    file_error = valid_file(fname)
    if file_error == "0":
        lines = (open(fname, 'r').read()).split()
        break
    else:
        print(file_error)

# Get input excluded words file
while True:
    flag = (input("Would you like to supply a list of words not to use? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    excluded = []
    if yn_error == "y":
        while True:
            fname = (input("Enter name of file containing characters not to be used: ").lower()).strip()
            file_error = valid_file(fname)
            if file_error == "0":
                excluded = (open(fname, 'r').read()).split()
                break
            else:
                print(file_error)
        break
    elif yn_error == "n":
        excluded = []
        break
    else:
        print(yn_error)

# Get input start word
while True:
    start = (input("Enter start word: ").lower()).strip()
    start_error = valid_start(start, lines)
    if start_error == "0":
        break
    else:
        print(start_error)

# Create an array and fill it with words from the list with the same length as the starting word
words = make_word_list(start,lines, excluded)

# Get input target word
while True:
    target = (input("Enter target word: ").lower()).strip()
    target_error = valid_target(start, target, words)
    if target_error == "0":
        break
    else:
        print(target_error)

# Get input shortest or longest path
short = False
while True:
    flag = (input("Would you like the short route? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    if yn_error == "y":
        short = True
        break
    elif yn_error == "n":
        break
    else:
        print(yn_error)

count = 0
path = [start]
seen = {start: True}
# Conduct first iteration of word ladder
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")
