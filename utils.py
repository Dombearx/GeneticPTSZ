

class Task:
    def __init__(self, p, r, d, number):
        # czas przetwarzania
        self.p = int(p)
        # czas gotowosci
        self.r = int(r)
        # oczekiwany czas zakonczenia
        self.d = int(d)
        # numer w pliku
        self.number = number


def checkInputFile(inputFileName):
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.split(" ")
            tasks.append(Task(p, r, d, index))

    inputFile.close()

    for task in tasks:
        if (task.r >= task.d):
            return False

        if (task.d - task.r < task.p):
            return False

        if(task.p <= 0):
            return False

    return True


def readInputFile(inputFileName):
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.split(" ")
            tasks.append(Task(p, r, d, index))
        else:
            # First line
            numberOfTasks = line

    return numberOfTasks, tasks


def readSolutionFile(solutionFileName):
    solutionFile = open(solutionFileName, "r")

    lines = []

    for index, line in enumerate(solutionFile):
        if(index != 0):
            lines.append(line.split(" "))
        else:
            # First line
            sum = line

    return sum, lines


def calculateSum(inputFileName, solution):
    """calculate sum of delays

    Arguments:
        inputFileName {string} -- file with input data
        solution {list} -- list with tasks associated to machines
    """
    inputFile = open(inputFileName, "r")
    tasks = []

    for index, line in enumerate(inputFile):
        # ignore first line
        if(index != 0):
            p, r, d = line.split(" ")
            tasks.append(Task(p, r, d, index))

    inputFile.close()
    sum = 0
    currentTime = 0

    for line in solution:
        for taskNumber in line:
            currentTime = tasks[int(taskNumber) - 1].r if tasks[int(taskNumber) -
                                                                1].r > currentTime else currentTime
            currentTime += tasks[int(taskNumber) - 1].p
            sum += max(0, currentTime - tasks[int(taskNumber) - 1].d)
        currentTime = 0

    return sum


def calculateFittnesValue(tasks, solution):

    sum = 0
    currentTime = 0

    for line in solution:
        for taskNumber in line:
            currentTime = tasks[int(taskNumber) - 1].r if tasks[int(taskNumber) -
                                                                1].r > currentTime else currentTime
            currentTime += tasks[int(taskNumber) - 1].p
            sum += max(0, currentTime - tasks[int(taskNumber) - 1].d)
        currentTime = 0

    return sum


def makeTxt(sum, lines, outputName):
    file = open(outputName, "w")
    file.write(str(sum) + "\n")
    for line in lines:
        file.write(line + "\n")
    file.close()


def makeSimpleLogFile(lines, outputName):
    file = open(outputName, "w")
    for value in lines:
        file.write(str(value) + "\t")
    file.close()


def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


def generateOutputFile(sum, solution, outputName):
    lines = []
    space = " "
    for line in solution:
        lines.append(space.join(map(str, line)))
    makeTxt(sum, lines, outputName)
