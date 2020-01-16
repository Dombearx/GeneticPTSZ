import math
import utils
import numpy as np
import pprint as pp


def sortByR(taskList):
    return sorted(taskList, key=lambda x: x.r, reverse=False)


def sortByD(taskList):
    return sorted(taskList, key=lambda x: x.d, reverse=False)


def getFirstFreeMachine(currentTimes):
    minTime = min(currentTimes)
    return currentTimes.index(minTime)


def generateSolution(n, numberOfMachines, tasks):

    solution = []
    for _ in range(numberOfMachines):
        solution.append([])

    tasks = sortByR(tasks)

    currentTimes = []
    for _ in range(numberOfMachines):
        currentTimes.append(0)

    while len(tasks) != 0:

        machine = getFirstFreeMachine(currentTimes)
        currentTime = currentTimes[machine]

        currentReadyTasks = []

        while(len(currentReadyTasks) == 0):
            for task in tasks:
                if task.r <= currentTime:
                    currentReadyTasks.append(task)
                else:
                    break

            if(len(currentReadyTasks) == 0):
                currentTimes[machine] = tasks[0].r
                machine = getFirstFreeMachine(currentTimes)
                currentTime = currentTimes[machine]

        sortedReadyTasks = sortByD(currentReadyTasks)

        task = sortedReadyTasks[0]
        solution[machine].append(task.number)

        tasks.remove(task)

        currentTimes[machine] = max(currentTimes[machine],
                                    task.r) + task.p

    return solution


'''
indeks = "132207"

nList = [int(x) for x in np.linspace(50, 500, 10)]
numberOfMachines = 4

for n in nList:
    inputFile = "in" + indeks + "_" + str(n) + ".txt"
    outputFile = "out" + indeks + "_" + str(n) + ".txt"

    solution = generateSolution(n, numberOfMachines, inputFile)

    sum = utils.calculateSum(inputFile, solution)

    utils.generateOutputFile(sum, solution, outputFile)
'''
