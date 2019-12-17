import utils
import random
import pprint as pp


class TaskOnMachine:
    def __init__(self, task, machine, priority):
        # zadanie
        self.task = task
        # do jakiej maszyny jest przypisane
        self.machine = int(machine)
        # piorytet
        self.priority = int(priority)


class Individual():
    tasksOnMachines = []
    tasks = []
    fittnesValue = -1
    solution = []
    translatedSolution = []

    def __init__(self, tasks):
        self.tasks = tasks

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

        for i in range(0, 4):
            self.translatedSolution.append([])

        for i in range(0, 4):
            self.translatedSolution[i] = [
                x.task.number for x in self.solution[i]]

    def getTranslatedSolution(self):
        return self.translatedSolution

    def calculateFittnesValue(self):
        if(self.translatedSolution == []):
            self.translateSolution()
        self.fittnesValue = utils.calculateFittnesValue(
            self.tasks, self.translatedSolution)

    def generateFirstSolution(self):
        priority = []
        for i in range(0, 4):
            priority.append(0)
        for task in self.tasks:
            machine = random.randint(0, 3)
            self.tasksOnMachines.append(
                TaskOnMachine(task, machine, priority[machine]))
            priority[machine] += 1
        self.translateSolution()

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
        return other

    def getFittnesValue(self):
        if self.fittnesValue == -1:
            self.calculateFittnesValue()
        return self.fittnesValue


class Population:
    individuals = []
    populationSize = -1

    def __init__(self, populationSize):
        self.populationSize = populationSize

    def generateIndividuals(self, tasks):
        for i in range(0, populationSize):
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
        for individual in self.individuals:
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
        #print("randomNumber", randomNumber)
        for id, fittnesSum in ranking:
           # print("fittnesSum", fittnesSum)
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
            if (fittnesSum > randomNumber):
                del self.individuals[id]
                return True
        return True

    def addIndividual(self, individual):
        self.individuals.append(individual)

    def evolution(self):
        print("---------------- Evolution start ----------------")
        first = self.select()
        second = self.select()

        print("1st parent fittness: ", first.getFittnesValue())
        print("2nd parent fittness: ", second.getFittnesValue())
        newIndividual = first.crossover(second)
        newIndividual.mutate()

        print("child fittness: ", newIndividual.getFittnesValue())
        self.remove()
        self.addIndividual(newIndividual)

        print("---------------- Evolution done ----------------")
        return True


##MAIN##
numberOfTasks, tasks = utils.readInputFile("input\\in132207_10.txt")

populationSize = 10

population = Population(populationSize)
population.generateIndividuals(tasks)
population.generateFirstSolutions()
# pp.pprint(population.getBestIndividual().getFittnesValue())
# pp.pprint(population.select())
# print("done")

for i in range(0, 100):
    pp.pprint(population.getBestIndividual().getFittnesValue())
    population.evolution()
