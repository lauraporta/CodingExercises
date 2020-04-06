
def containsRepetitions(x, numberOfRows):
    isRepeated = 0
    for n in range(numberOfRows):
        repetitions = 0
        for o in x:
            if n == (o - 1):
                repetitions += 1
        if repetitions != 1:
            isRepeated = 1
            break
    return isRepeated

numberOfMatrices = int(input())
solution = []

for i in range(numberOfMatrices):
    numberOfRows = int(input())
    m = []

    rowsRepEls = 0
    for j in range(numberOfRows):
        tmp =[]
        r = []
        row = input()
        tmp = row.split(' ')
        for k in range(numberOfRows):
            r.append(int(tmp[k]))
        rowsRepEls += containsRepetitions(r, numberOfRows)
        m.append(r)

    colsRepEls = 0
    trace = 0
    for j in range(numberOfRows):
        trace += m[j][j]
        c = []
        for k in range(numberOfRows):
            c.append(m[k][j])
        colsRepEls += containsRepetitions(c, numberOfRows)

    solution.append("Case #{}: {} {} {}".format(i + 1, trace, rowsRepEls, colsRepEls))

for i in range(numberOfMatrices):
    print(solution[i])


