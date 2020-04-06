
T = int(input())

solution = []

for b in range(T):
    N = int(input())
    taskTime = []
    unsortedTasks = []
    schedule = ""
    schedule2 = []

    for i in range(N):
        tmp = input().split(" ")
        taskTime.append((int(tmp[0]), int(tmp[1])))
        unsortedTasks.append((int(tmp[0]), int(tmp[1])))

    taskTime.sort()

    for i in range(N):
        if schedule == "IMPOSSIBLE":
            continue
        else:
            if i == 0:
                schedule += "C"
            else:
                splt = list(schedule)
                lastJpos = 0
                lastCpos = 0
                for j in range(i):
                    if splt[j] == "J":
                        lastJpos = j
                    if splt[j] == "C":
                        lastCpos = j
                if taskTime[i][0] >= taskTime[lastCpos][1]:
                    schedule += "C"
                elif lastJpos == 0:
                    schedule += "J"
                elif taskTime[i][0] >= taskTime[lastJpos][1]:
                    schedule += "J"
                else:
                    schedule = "IMPOSSIBLE"

    if schedule == "IMPOSSIBLE":
        solution.append(schedule)
    else:
        repetitions = 0
        for j in range(N):
            idx = 0
            if repetitions == 1:
                continue
            else:
                for k in range(N):
                    if repetitions == 1:
                        break
                    elif taskTime[k] == unsortedTasks[j]:
                        times = taskTime.count(taskTime[k])
                        if times == 1:
                            idx = k
                            repetitions = 0
                        elif times > 1:
                            repetitions = 1
                            randomPerson = "CJ"

            if repetitions == 0:
                schedule2.append(list(schedule)[idx])
            else:
                schedule2.append(randomPerson)
        solution.append(''.join(schedule2))
        schedule2.clear()


for i in range(T):
    print("Case #{}: {}".format(i + 1, solution[i]))
