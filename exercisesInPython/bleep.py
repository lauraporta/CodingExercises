from cs50 import get_string
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python bleep.py path/to/dictionary")

    words = []
    load(sys.argv[1], words)

    imput = get_string("What message would you like to censor?\n")
    splittedImput = []
    splittedImput = imput.split(' ')

    for word in splittedImput:
        if str.lower(word) in words:
            print("*" * len(word) + " ", end="")
        else:
            print(word + " ", end="")

    print()



def load(dictionary, words):
    file = open(dictionary, "r")
    for line in file:
        words.append(line.rstrip("\n"))
    file.close()
    return True

if __name__ == "__main__":
    main()
