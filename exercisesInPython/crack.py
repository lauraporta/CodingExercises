import sys
import crypt

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python crack.py hash")

    #if len(sys.argv[1]) != 13:
       # sys.exit("Usage: python crack.py hash")

    salt = []
    for i in range(2):
        salt.append(sys.argv[1][i])

    searchDepth = 40
    bruteForce(sys.argv[1], searchDepth, salt)


def bruteForce(givenHash, searchDepth, salt):
    for i in range(searchDepth):
        psw = ["@"] * (i + 1)
        bruteForceRecursive(givenHash, psw, 0, salt)


def bruteForceRecursive(givenHash, psw, cursor, salt):
    for i in range(26*2):
        psw[cursor] = changeChar(ord(psw[cursor]))

        if crypt.crypt(''.join(psw), ''.join(salt)) == givenHash:
            print(''.join(psw))
            sys.exit()
        else:
            if (cursor + 1) < len(psw):
                cursor += 1
                bruteForceRecursive(givenHash, psw, cursor, salt)
                cursor -= 1


def changeChar(char):
    if (char > 63 and char < 90) or (char > 96 and char < 122):   # uppercase or lowercase
        return str(chr(char + 1))

    elif char == 90:
        return 'a'

    elif char == 122:
        return 'A'

    else:
        return '0'


if __name__ == "__main__":
    main()