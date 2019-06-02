# The eight queens puzzle is the problem of
# placing eight chess queens on an 8×8 chessboard
# so that no two queens threaten each other; thus,
# a solution requires that no two queens share the
# same row, column, or diagonal.

import numpy as np
import random
import time
import operator

POPULATION_SIZE = 500
MUTATION_RATE = 30
FITNESS_THRESHOLD = 3


class Genome():
    chromosomes = []
    fitness = 99


class GenericAlgorithm():
    def __init__(self):
        self.population = []
        self.generation = 0
        self.result = None

    def CreateNewPopulation(self, size):
        for x in range(size):
            newGenome = Genome()
            newGenome.chromosomes = random.sample(range(0, 8), 8)
            newGenome.fitness = self.Evaluate(newGenome.chromosomes)
            self.population.append(newGenome)

    def SetChessBoard(self, chromo):
        chessboard = np.zeros((8, 8), dtype=int)
        for i in range(8):
            y = chromo[i]
            chessboard[y][i] = 1
        return chessboard

    # Evaluating system controls horizontal and cross direction.
    # Every collision between another queen increases fitness value.
    # Best fitness value is zero.
    def Evaluate(self, chromosomes):
        chessboard = self.SetChessBoard(chromosomes)
        calculated_fitness = 0

        # Horizontal Control
        for i in range(8):
            count = np.count_nonzero(chessboard[i])
            if count > 1:
                calculated_fitness += count - 1

        # Cross Control
        for y in range(8):
            count = 0
            for x in range(8):
                if chessboard[x + y, x] == 1:
                    count += 1
                if (x + y) >= 7:
                    break
            if count > 1:
                calculated_fitness += count - 1

        for y in range(1, 8):
            count = 0
            for x in range(8):
                if chessboard[x, x + y] == 1:
                    count += 1
                if (x + y) >= 7:
                    break
            if count > 1:
                calculated_fitness += count - 1

        for y in range(0, 8):
            count = 0
            for x in range(0, 8):
                if chessboard[y + x, 7 - x] == 1:
                    count += 1
                if (y + x) >= 7:
                    break
            if count > 1:
                calculated_fitness += count - 1

        for y in range(0, 8):
            count = 0
            for x in range(0, 7 - y):
                if chessboard[x, (6 - y) - x] == 1:
                    count += 1
                if (x) >= 7:
                    break
            if count > 1:
                calculated_fitness += count - 1

        return calculated_fitness

    def RouletteWheelSelection(self):
        max = sum(genom.fitness for genom in self.population)
        pick = random.uniform(0, max)
        current = 0
        for genom in self.population:
            current += genom.fitness
            if current > pick:
                return genom

    def OnePointCrossover(self):
        parent1 = self.RouletteWheelSelection().chromosomes
        parent2 = self.population[random.randrange(0, len(self.population))].chromosomes

        point = random.randint(2, 6)
        child = Genome()
        child.chromosomes = parent1[0:point]
        child.chromosomes.extend(parent2[point:8])
        child.fitness = self.Evaluate(child.chromosomes)

        if random.randrange(0, 100) < MUTATION_RATE:
            self.Mutation(child.chromosomes)
        else:
            self.population.append(child)

    def Mutation(self, chromo):
        chromo[random.randrange(0, 8)] = random.randrange(0, 8)
        newGenome = Genome()
        newGenome.chromosomes = chromo
        newGenome.fitness = self.Evaluate(newGenome.chromosomes)
        self.population.append(newGenome)

    def KillWitness(self):
        for genom in self.population:
            if genom.fitness > FITNESS_THRESHOLD:
                self.population.remove(genom)

    def ControlResult(self):
        for genom in self.population:
            if(genom.fitness < 1):
                self.result = genom.chromosomes

    def Start(self):
        # If can't found result, reset and try again
        while self.result is None:
            self.population = []
            self.generation = 0

            self.CreateNewPopulation(POPULATION_SIZE)
            print("******New Population Created******")
            while self.generation < 30 and self.result is None:

                for x in range(int(len(self.population) / 2)):
                    self.OnePointCrossover()

                self.KillWitness()
                self.ControlResult()
                self.generation += 1
                print("POPULATION=", len(self.population), "GENERATION=", self.generation)

        chessboard = self.SetChessBoard(self.result)
        print(chessboard)
        print("Found in {0}. generation".format(self.generation))


GenericAlgorithm().Start()
