# application information
__author__ = "Jordan Schurmann, Luke Reynolds"
__email__ = "jordan.schurmann@gmail.com, lreynolds188@gmail.com"
__version__ = "1.0.1"
__website__ = "http://lukereynolds.net/"

def same(item, target):
    print("err")

def build(pattern, words, seen, list):
    print("err")

def findPath(word, words, target, path):
    list = words
    return True


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
path = [start] # create a list and input the starting word
if findPath(start, target, words, path):
    print(len(path) - 1, path)
else:
    print("No path found")
