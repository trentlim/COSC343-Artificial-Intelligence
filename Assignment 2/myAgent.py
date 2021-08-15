import numpy as np
import random

playerName = "myAgent"
nPercepts = 75  # This is the number of percepts
nActions = 5  # This is the number of actions

# Training schedule
trainingSchedule = [("random", 1000), ("self", 0)]


# Creature/agent class
class MyCreature:

    def __init__(self):
        # Creates a matrix of weights as the creature's chromosome
        # 75 rows, for each percept
        # 5 columns, for each action
        # 375 values in total
        # Each value in the matrix is initially set to a random float
        # between 0 and 1 with a uniform distribution
        self.chromosome = np.random.uniform(0, 1, (nPercepts, nActions))

        # Create a fitness variable for the creature
        self.fitness = 0

    # Function that maps the creature's percepts to actions using its chromosome
    def AgentFunction(self, percepts):
        actions = np.zeros(nActions)
        percepts = percepts.flatten()

        # For each value in the chromosome, multiply it by its corresponding percept
        # The largest value in each column, after being multiplied, is stored in
        # the 'actions' list as the weight for the action in that index
        for i in range(nPercepts):
            for j in range(nActions):
                x = percepts[i] * self.chromosome[i][j]
                actions[j] += x

        return actions


# Creates a list of the new generation with the old population as input
# The new generation is the same length as the old population (N)
# Returns avg_fitness and new_population
def newGeneration(old_population):
    # This function returns a list of the 'new_population' that is the same length as 'old_population' (N)
    # This function also returns average fitness of the old_population

    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros(N)

    # This loop iterates over each agent in the old population and determines the fitness of
    # each agent in the population based on attributes provided by the game engine
    for n, creature in enumerate(old_population):
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        # creature.squares_visited - how many different squares the creature visited
        # creature.bounces - how many times the creature bounced

        b = creature.strawb_eats
        e = creature.enemy_eats
        v = creature.squares_visited
        x = creature.bounces

        # Fitness function which determines fitness of each agent
        # Adds fitness value to list of fitness for all agents
        # Updates 'fitness' variable for each creature
        fitness[n] = 10*e + 5*b + v - x/5
        creature.fitness = fitness[n]

    # Parent selection method
    # Randomly selects a list of size s of agents from the old population
    # Returns the two fittest members of that list as parents
    def selectParents(s):
        tournament = list()

        for i in range(s):
            tournament.append(old_population[random.randint(0, N - 1)])

        tournament.sort(key=lambda c: c.fitness, reverse=True)
        parent1 = tournament[0]
        parent2 = tournament[1]

        return parent1, parent2

    # Crossover method
    # Uniform crossover: each gene has the same chance of being from either parent
    # Returns child with genes crossed over
    def crossover(parent1, parent2):
        child = MyCreature()

        for i in range(nPercepts):
            for j in range(nActions):
                if random.random() < 0.5:
                    child.chromosome[i][j] = parent1.chromosome[i][j]
                else:
                    child.chromosome[i][j] = parent2.chromosome[i][j]

        return child

    # Mutation method
    # Each gene in the creature's chromosome has probability p of being mutated
    # If a gene is mutated, its value is set to a random float between 0 and 1
    def mutate(child, p):
        for i in range(nPercepts):
            for j in range(nActions):
                if random.random() < p:
                    child.chromosome[i][j] = random.uniform(0, 1)
        return child

    # Create new population
    new_population = list()

    # This loop creates N creatures and adds each creature to the new population
    # The creatures' chromosomes are determined by functions which select 2 parents from the old population
    # based on fitness, and crosses over the parents' chromosomes to create the child's chromosome
    # Then, each gene of a child's chromosome has a probability of being mutated
    for n in range(N):
        # PARENT SELECTION
        parents = selectParents(8)
        parent1 = parents[0]
        parent2 = parents[1]

        # CROSSOVER
        new_creature = crossover(parent1, parent2)

        # MUTATION
        new_creature = mutate(new_creature, 0.005)

        # Add the new agent to the new population
        new_population.append(new_creature)

    # Calculate average fitness
    avg_fitness = np.mean(fitness)

    # Return new
    return new_population, avg_fitness
