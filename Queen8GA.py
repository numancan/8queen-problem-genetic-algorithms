import numpy as np
import random
import time
import operator

POPULATION_SIZE = 100
MUTATION_RATE = 20
FITNESS_THRESHOLD = 2


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
            newGenome.fitness = self.CalculateFitness(newGenome.chromosomes)
            self.population.append(newGenome)

    def SetChessBoard(self, chromo):
        chessboard = np.zeros((8, 8), dtype=int)
        for i in range(8):
            y = chromo[i]
            chessboard[y][i] = 1
        return chessboard

    def CalculateFitness(self, chromosomes):
        chessboard = self.SetChessBoard(chromosomes)
        calculated_fitness = 0

        # Horizantal Control
        for i in range(8):
            count = np.count_nonzero(chessboard[i] == 1)
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

    def roulette_selection(self, fitness):
        sorted_indexed_weights = sorted(enumerate(fitness), key=operator.itemgetter(1))
        indices, sorted_weights = zip(*sorted_indexed_weights)
        tot_sum = sum(sorted_weights)
        prob = [x / tot_sum for x in sorted_weights]
        cum_prob = np.cumsum(prob)
        random_num = random.random()

        for index_value, cum_prob_value in zip(indices, cum_prob):
            if random_num > cum_prob_value:
                return index_value

    def SelectParentMakeCrossover(self):

        fitness_list = [genom.fitness for genom in self.population]
        index = self.roulette_selection(fitness_list)
        if index is not None:
            selected_genom = self.population[index]
        else:
            selected_genom = self.population[random.randrange(0, len(self.population))]
        random_genom = self.population[random.randrange(0, len(self.population))]

        # If selected genom and random selected genom is same, try again
        if selected_genom == random_genom:
            self.SelectParentMakeCrossover()
        else:
            self.Crossover(random_genom.chromosomes, selected_genom.chromosomes)

    def Crossover(self, parent1, parent2):
        point = random.randint(2, 6)
        child = Genome()
        child.chromosomes = parent1[0:point]
        child.chromosomes.extend(parent2[point:8])
        child.fitness = self.CalculateFitness(child.chromosomes)

        self.population.append(child)
        if random.randrange(0, 100) < MUTATION_RATE:
            self.Mutation(child.chromosomes)

        child = Genome()
        child.chromosomes = parent2[0:point]
        child.chromosomes.extend(parent1[point:8])
        child.fitness = self.CalculateFitness(child.chromosomes)
        self.population.append(child)
        if random.randrange(0, 100) < MUTATION_RATE:
            self.Mutation(child.chromosomes)

    def KillWitness(self):
        for genom in self.population:
            if genom.fitness > FITNESS_THRESHOLD:
                self.population.remove(genom)

    def Mutation(self, chromo):
        chromo[random.randrange(0, 8)] = random.randrange(0, 8)
        newGenome = Genome()
        newGenome.chromosomes = chromo
        newGenome.fitness = self.CalculateFitness(newGenome.chromosomes)
        self.population.append(newGenome)

    def ControlResult(self):
        for genom in self.population:
            if(genom.fitness < 1):
                self.result = genom.chromosomes

    def Start(self):
        while self.result is None:

            self.population = []
            self.generation = 0

            # Create new population have random chromosomes
            self.CreateNewPopulation(POPULATION_SIZE)
            print("******Created New Population******")
            # Kill population in after 3 generation
            while self.generation < 3 and self.result is None:
                # Calculate every new person fitness
                for genom in self.population:
                    genom.fitness = self.CalculateFitness(genom.chromosomes)

                for x in range(len(self.population)):
                    self.SelectParentMakeCrossover()

                self.KillWitness()
                self.ControlResult()
                self.generation += 1
                print("POPULATION=", len(self.population), "GENERATION=", self.generation)

        chessboard = self.set_chessboard(self.result)
        print(chessboard)
        print("Found in {0}. generation".format(self.generation))


GenericAlgorithm().Start()
