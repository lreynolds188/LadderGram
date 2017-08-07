import os
import re

# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.15"
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
    :param seen: Dictionary with words and count of letter matches for each word
    :type seen: dict
    :param list: List of currently viewed words - don't want to reuse them
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

    # Determine whether start and target letters match. If greater than 0 then identify matching letters so that
    # these letters are excluded from the new pattern. All new words are to have these letters at a minimum.
    if (sum(1 for (c, t) in zip(start, target) if c == t)) > 0:
        for i in range(len(start)):
            # Compare the new start word to the target word and return a list containing indexes
            # of matched letters.  E.g. [0,6] indicates letter matches at the first and seventh letters.
            matchedletters = [i for i, x in enumerate(zip(start, target)) if all(y == x[0] for y in x)]
    for i in range(len(start)):
        # For each letter position, only build a pattern for letter positions that have not already been found.
        if i not in matchedletters:
            # Add all words matching the pattern to the list. Only process patterns where the letter
            # has not been found. Pattern is of type lead: ".ead", "l.ad", "le.d", "lea.")
            list += build(start[:i] + "." + start[i + 1:], words, seen, list)

    # If the list is empty (no matching words found) - Exit the iteration and process the next item if one exists.
    # If no other item exists then exit as No Path Found.
    if len(list) == 0:
        return False

    # Sort the list by number of matches and alphabetically.  If reverse is specified sort by
    # highest number of matching letters first and then alphabetically.
    list = sorted([(same(w, target), w) for w in list], reverse=short)

    # For each matched pair in the sorted list.
    for (match, item) in list:

        # If the current word matches target or 1 letter off target.
        if match >= len(target) - 1:
            if match == len(target) - 1:
                # Append the word to the path and exit the recursion, as we have found the last word.
                path.append(item)
            return True
        # For each word in the current list add it too seen so that future searches exclude the word.
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
    Function to validate input for start word.

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
    Function to validate input for target word.

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


def valid_yn(flag):
    """
    Function to validate y/n options.

    :param flag: String indicating yes or no
    :type flag: str
    :return: Integer indicating whether data is valid
    :rtype: int

    """

    yes_or_no = ['y', 'n']
    if len(flag) == 1:  # flag must be one character
        if flag.isalpha():  # flag must be alphabetic
            if flag in yes_or_no:  # target word must be Y or N
                if flag == 'y':
                    return 0  # 0 = y
                else:
                    return 99  # 99 = n
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
    Function to return error message depending upon error code provided.

    :param error: Error code received from the various validation functions
    :type error: int
    :return: Error message for the integer
    :rtype: str

    """
    message = ""
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

# Get input dictionary file
while True:
    fname = (input("Enter dictionary name: ").lower()).strip()
    file_error = valid_file(fname)
    if file_error == 0:
        lines = (open(fname, 'r').read()).split()  # open and read file
        break
    else:
        print(errormessage(file_error))

# Get input excluded words file
while True:
    flag = (input("Would you like to supply a list of words not to use? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    excluded = []
    if yn_error == 0:  # Yes
        while True:
            fname = (input("Enter name of file containing characters not to be used: ").lower()).strip()
            file_error = valid_file(fname)
            if file_error == 0:
                excluded = (open(fname, 'r').read()).split()  # open and read file
                break
            else:
                print(errormessage(file_error))
        break
    elif yn_error == 99:  # No
        break
    else:
        print(errormessage(yn_error))

# Get input start word
while True:
    start = (input("Enter start word: ").lower()).strip()
    start_error = valid_start(start, lines)
    if start_error == 0:
        break
    else:
        print(errormessage(start_error))

# Create an array and fill it with words from the list with the same length as the starting word
# excluded will be blank if the user has decided not to supply any words to omit
words = []
for line in lines:
    word = line.rstrip()
    if len(word) == len(start):
        if (word == start) or (word not in excluded):  # If the start word is in the excluded list, do not exclude it
            words.append(word)

# Get input target word
while True:
    target = (input("Enter target word: ").lower()).strip()
    target_error = valid_target(start, target, words)
    if target_error == 0:
        break
    else:
        print(errormessage(target_error))

# Get input shortest or longest path
short = False
while True:
    flag = (input("Would you like the short route? y/n: ").lower()).strip()
    yn_error = valid_yn(flag)
    if yn_error == 0:  # Yes
        short = True
        break
    elif yn_error == 99:  # No
        break
    else:
        print(errormessage(yn_error))

count = 0
path = [start]
seen = {start: True}
# Conduct first iteration of word ladder
if find(start, words, seen, target, path):
    path.append(target)
    print(len(path) - 1, path)
else:
    print("No path found")
