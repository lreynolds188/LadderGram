import os
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.11"
__website__ = "http://lukereynolds.net/"


def same(item, target):
    """
    Function returns the number of letters for each item that match that target word

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
    Function builds a list of word that match the pattern sent to the function

    :param pattern: Pattern changes on each evocation - e.g. lead: ".ead", "l.ad", "le.d", "lea.")
    :type pattern: str
    :param words: List of all words
    :type words: list
    :param seen: Dictionary with words and count of letter matches for each word
    :type seen: dict
    :param list: List of currently viewed words - dont want to reuse them
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
    :type seen: list
    :param target: Target word
    :type target: str
    :param path: Current path to the target word
    :type path: List
    :return: True or False if found or no path
    :rtype: Boolean

    """
    setword = []
    list = []

    """
    If any letters of the start and target match
    """
    if same(start, target) > 0:
        for i in range(len(start)):
            """
            Check if new start value is within 1 character of target
            """
            if path[-1][i] == target[i]:
                setword.append(i)
    """
    For each word
    """
    for i in range(len(start)):
        """
        If not a word containing target letters
        """
        if i not in setword:
            """
            Add the return value of the build function to the list when sent the pattern of the word
            (e.g. lead: ".ead", "l.ad", "le.d", "lea.")
            """
            list += build(start[:i] + "." + start[i + 1:], words, seen, list)
    """
    If the list is empty
    """
    if len(list) == 0:
        return False
    """
    Sort the list into pairs showing the current words closeness to the target word followed by the current
    word (e.g. the word 'load' and 'gold' have 2 of the same letters so it will be represented by (2, 'load'))
    """
    list = sorted([(same(w, target), w) for w in list], reverse=short)
    """
    For each pair in the list
    """
    for (match, item) in list:
        """
        If the current word matches or 1 letter off
        """
        if match >= len(target) - 1:
            """
            If the current word amount of matching letter is equal to the length of the target word minus 1
            """
            if match == len(target) - 1:
                """
                Append the corresponding word to the path
                """
                path.append(item)
            return True
        """
        Mark that the word has been looked at, so that it is excluded in future reviews
        """
        seen[item] = True
    """
    Set the word to reiterate down the loop.  Start becomes new item
    """
    for (match, item) in list:
        path.append(item)
        if find(item, words, seen, target, path):
            return True
        path.pop()


def valid_file(fname):
    """
    Function to validate input file

    :param fname: File name input
    :type fname: str
    :return: Integer indicating whether file data is valid
    :rtype: int

    """
    try:
        if os.stat(fname).st_size > 0:  # if filename contains data
            return 0
        else:
            return 1
    except OSError:  # if no file of that name found
        return 2


def valid_start(start, lines):
    """
    Function to validate input for start word

    :param start: Start word input
    :type start: str
    :param lines: List of dictionary words
    :type lines: list
    :return: Integer indicating whether data is valid
    :rtype: int

    """
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


def valid_target(start, target, words):
    """
    Function to validate input for target word

    :param start: Start word input
    :type start: str
    :param target: Target word input
    :type target: str
    :param words: List of dictionary words
    :type words: list
    :return: Integer indicating whether data is valid
    :rtype: int

    """
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
    """
    Function to validate y/n options

    :param flag: String indicating yes or no
    :type flag: str
    :return: Integer indicating whether data is valid
    :rtype: int

    """
    yes_or_no = ['y', 'n']
    if len(flag) == 1:
        if flag.isalpha():
            if flag in yes_or_no:
                if flag == 'y':
                    return 0
                else:
                    return 99
            else:
                return 10
        else:
            return 11
    elif len(flag) > 1:
        return 12
    else:
        return 13


def errormessage(error):
    """
    Function to print all errors depending upon error message returned.

    :param error: Error code received from the various validation functions
    :type error: int
    :return: Error message for the integer
    :rtype: str

    """
    if error == 1:
        message = "Selected file is empty....please reenter"
    elif error == 2:
        message = "Can not find the file....please reenter"
    elif error == 3:
        message = "Start word not in list of words....please reenter"
    elif error == 4:
        message = "Start word must contain more than one letter....please reenter"
    elif error == 5:
        message = "Start word must contain only letters....please reenter"
    elif error == 6:
        message = "Target word not in list of words....please reenter"
    elif error == 7:
        message = "Target word must be different from Start word....please reenter"
    elif error == 8:
        message = "Target word must be same length as Start word....please reenter"
    elif error == 9:
        message = "Target word must only contain letters....please renter"
    elif error == 10:
        message = "Please enter Y or N only"
    elif error == 11:
        message = "Please enter letters Y or N only"
    elif error == 12:
        message = "Please enter only one character"
    elif error == 13:
        message = "Please enter a character"
    return message


"""
Get Input dictionary
"""
while True:
    fname = (input("Enter dictionary name: ").lower()).strip()
    file_error = valid_file(fname)
    if file_error == 0:
        # open and read file
        lines = (open(fname, 'r').read()).split()
        break
    else:
        print(errormessage(file_error))
"""
Get excluded words
"""
while True:
    flag = (input("Would you like to supply a list of words not to use? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    excluded = []
    if yn_error == 0:
        while True:
            fname = (input("Enter name of file containing characters not to be used: ").lower()).strip()
            file_error = valid_file(fname)
            if file_error == 0:
                # open and read file
                excluded = (open(fname, 'r').read()).split()
                break
            else:
                print(errormessage(file_error))
        break
    elif yn_error == 99:
        break
    else:
        print(errormessage(yn_error))

"""
Get start word
"""
while True:
    start = (input("Enter start word: ").lower()).strip()
    start_error = valid_start(start, lines)
    if start_error == 0:
        break
    else:
        print(errormessage(start_error))
"""
Create an array and fill it with words from the list with the same length as the starting word
excluded will be blank if the user has decided not to supply any words to omit
"""
words = []
for line in lines:
    word = line.rstrip()
    if len(word) == len(start):
        # If the start word is in the excluded list, do not exclude it
        if (word == start) or (word not in excluded):
            words.append(word)

"""
Get target word
"""
while True:
    target = (input("Enter target word: ").lower()).strip()
    target_error = valid_target(start, target, words)
    if target_error == 0:
        break
    else:
        print(errormessage(target_error))

"""
Get shortest or longest path
"""
short = False
while True:
    flag = (input("Would you like the short route? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    if yn_error == 0:
        short = True
        break
    elif yn_error == 99:
        break
    else:
        print(errormessage(yn_error))

count = 0
path = [start]
seen = {start: True}
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")