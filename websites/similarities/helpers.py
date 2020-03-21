from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    listA = list(a.split('\n'))
    listB = list(b.split('\n'))
    matching = []
    for string in listA:
        if (string in listB) and not (string in matching):
            matching.append(string)
    return matching


def sentences(a, b):
    """Return sentences in both a and b"""
    listA = list(sent_tokenize(a))
    listB = list(sent_tokenize(b))
    matching = []
    for string in listA:
        if (string in listB) and not (string in matching):
            matching.append(string)
    return matching


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    listA = list(subExtraction(a, n))
    listB = list(subExtraction(b, n))
    matching = []
    for string in listA:
        if (string in listB) and not (string in matching) and not (string == ''):
            matching.append(string)
    return matching


def subExtraction(s, n):
    dsj = []
    for i in range(len(s) - n + 1):
        dsj.append(s[i: (i + n)])
    return dsj