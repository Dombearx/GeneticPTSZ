import utils
import random
import pprint as pp
import copy
import solverListowy


class TaskOnMachine:
    def __init__(self, taskId, machine, priority):
        # zadanie
        self.taskId = taskId
        # do jakiej maszyny jest przypisane
        self.machine = int(machine)
        # piorytet
        self.priority = int(priority)


class Individual():

    def __init__(self, tasks):
        self.tasks = tasks
        self.tasksOnMachines = []
        self.fittnesValue = -1
        self.solution = []
        self.translatedSolution = []

    def sortByPriority(self, tasks):
        return sorted(tasks, key=lambda x: x.priority, reverse=False)

    def translateSolution(self):
        self.solution = []
        self.translatedSolution = []

        for i in range(0, 4):
            self.solution.append([])
        for taskOnMachine in self.tasksOnMachines:
            self.solution[taskOnMachine.machine].append(
                taskOnMachine)

        for i in range(0, 4):
            self.solution[i] = self.sortByPriority(self.solution[i])

        self.recalculatePriority()

        for i in range(0, 4):
            self.translatedSolution.append([])

        for i in range(0, 4):
            self.translatedSolution[i] = [
                x.taskId for x in self.solution[i]]

    def calculateFittnesValue(self):
        if(self.translatedSolution == []):
            self.translateSolution()
        self.fittnesValue = utils.calculateFittnesValue(
            self.tasks, self.translatedSolution)

    def readSolution(self, solution):
        for machineId, machine in enumerate(solution):
            for priority, taskId in enumerate(machine):
                self.tasksOnMachines.append(
                    TaskOnMachine(taskId, machineId, priority))
        self.translateSolution()

    def generateFirstSolution(self):
        for task in self.tasks:
            machine = random.randint(0, 3)
            priority = random.randint(0, len(tasks))

            self.tasksOnMachines.append(
                TaskOnMachine(task.number, machine, priority))

        self.translateSolution()

    def recalculatePriority(self):
        priority = []
        for _ in range(0, 4):
            priority.append(0)

        for machine in self.solution:
            for task in machine:
                task.priority = priority[task.machine]
                priority[task.machine] += 1

    def mutate(self):
        machine = random.randint(0, 3)
        task = random.randint(0, len(self.tasksOnMachines) - 1)
        maxpriority = 0
        for taskOnMachine in self.tasksOnMachines:
            if taskOnMachine.machine == machine:
                if taskOnMachine.priority > maxpriority:
                    maxpriority = taskOnMachine.priority

        priority = random.randint(0, maxpriority)

        self.tasksOnMachines[task].machine = machine
        self.tasksOnMachines[task].priority = priority

        self.translateSolution()
        self.calculateFittnesValue()
        return True

    def crossover(self, other):
        newIndividual = copy.deepcopy(other)
        crossPoint = random.randint(0, len(self.tasks))
        for i in range(0, crossPoint):
            newIndividual.tasksOnMachines[i] = self.tasksOnMachines[i]

        newIndividual.translateSolution()
        return newIndividual

    def getFittnesValue(self):
        if self.fittnesValue == -1:
            self.calculateFittnesValue()
        return self.fittnesValue


class Population:

    def __init__(self, populationSize):
        self.populationSize = populationSize
        self.individuals = []

    def generateIndividuals(self, tasks):
        self.tasks = tasks
        for _ in range(0, populationSize):
            self.individuals.append(Individual(tasks))

    def getBestIndividual(self):
        bestValue = self.individuals[0].getFittnesValue()
        bestIndividual = self.individuals[0]
        for individual in self.individuals[1:]:
            if individual.getFittnesValue() < bestValue:
                bestValue = individual.getFittnesValue()
                bestIndividual = individual

        return bestIndividual

    def generateFirstSolutions(self):

        listowy = solverListowy.generateSolution(
            len(self.tasks), 4, self.tasks)
        for individual in self.individuals[:int(len(self.individuals) / 2)]:
            individual.readSolution(listowy)

        for individual in self.individuals[int(len(self.individuals) / 2):]:
            individual.generateFirstSolution()

    def select(self):
        ranking = []
        sumOfValues = 0
        newSumOfValues = 0
        for individual in self.individuals:
            sumOfValues += individual.getFittnesValue()
        for id, individual in enumerate(self.individuals):
            newSumOfValues += sumOfValues - individual.getFittnesValue()
            ranking.append((id, newSumOfValues))

        randomNumber = random.randint(0, newSumOfValues)
        for id, fittnesSum in ranking:
            if (fittnesSum > randomNumber):
                return self.individuals[id]
        return None

    def remove(self):
        ranking = []
        fittnesValueSum = 0
        for id, individual in enumerate(self.individuals):
            fittnesValueSum += individual.getFittnesValue()
            ranking.append((id, fittnesValueSum))

        randomNumber = random.randint(0, fittnesValueSum)
        for id, fittnesSum in ranking:
            if (fittnesSum >= randomNumber):
                del self.individuals[id]
                return True
        return True

    def addIndividual(self, individual):
        self.individuals.append(individual)

    def evolution(self):
        #print("---------------- Evolution start ----------------")
        first = self.select()
        second = self.select()

        newIndividual = first.crossover(second)
        newIndividual.mutate()

        self.remove()
        self.addIndividual(newIndividual)

        #print("---------------- Evolution done ----------------")
        return True

    def addToLog(self, log):
        try:
            log.append(self.getBestIndividual().getFittnesValue())
        except:
            print("Erorr:", len(self.individuals))


##MAIN##
numberOfTasks, tasks = utils.readInputFile("input\\in132207_50.txt")

populationSize = 30

outputLog = []

population = Population(populationSize)
population.generateIndividuals(tasks)
population.generateFirstSolutions()

population.addToLog(outputLog)

best = 99999

for i in range(0, 100000):
    if population.getBestIndividual().getFittnesValue() < best:
        bestInd = population.getBestIndividual()
        best = bestInd.getFittnesValue()
        pp.pprint(bestInd.translatedSolution)
        print("Best in generation", str(i), "->",
              str(bestInd.getFittnesValue()))
    population.evolution()

utils.generateOutputFile(best, bestInd.translatedSolution, "out.txt")
