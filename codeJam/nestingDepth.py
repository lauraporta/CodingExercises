T = int(input())

solution = []
for i in range(T):
    charL = list(input())
    string = ""
    tmp = ""
    prv = 0

    for c in charL:
        intTmp = int(c)

        if prv < intTmp:
            tmp = ("(" * (intTmp - prv)) + c
        if prv == intTmp:
            tmp = c
        if prv > intTmp:
            tmp = (")" * (prv - intTmp)) + c 

        prv = intTmp
        string += tmp

    string += ")" * intTmp
    solution.append("Case #{}: {}".format(i + 1, string))
for i in range(T):
    print(solution[i])