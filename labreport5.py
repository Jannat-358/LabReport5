import random

def fitness(individual):
    non_attacking = 0
    for i in range(len(individual)):
        for j in range(i + 1, len(individual)):
            if abs(individual[i] - individual[j]) != abs(i - j):
                non_attacking += 1
    return non_attacking

def create_individual(n):
    individual = list(range(n))
    random.shuffle(individual)
    return individual


def selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, score in zip(population, fitnesses):
        current += score
        if current > pick:
            return individual


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child = parent1[:point] + [gene for gene in parent2 if gene not in parent1[:point]]
    return child


def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual


def print_board(state):
    print("\nChessboard:")
    for row in range(len(state)):
        line = ""
        for col in range(len(state)):
            if state[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)


def genetic_algorithm(N, POP_SIZE=100, MUTATION_RATE=0.03, MAX_GENERATIONS=1000):
    population = [create_individual(N) for _ in range(POP_SIZE)]
    max_fitness = N * (N - 1) // 2

    for generation in range(MAX_GENERATIONS):
        fitnesses = [fitness(ind) for ind in population]

        if max_fitness in fitnesses:
            solution = population[fitnesses.index(max_fitness)]
            print(f"\n✅ Solution found in generation {generation}:")
            print(solution)
            print_board(solution)
            return solution

        new_population = []
        for _ in range(POP_SIZE):
            parent1 = selection(population, fitnesses)
            parent2 = selection(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, MUTATION_RATE)
            new_population.append(child)

        population = new_population

    print("\n❌ No optimal solution found.")
    return None


if __name__ == "__main__":
    try:
        N = int(input("Enter the number of Queens (N ≥ 4): "))
        if N < 4:
            print("N should be 4 or greater.")
        else:
            genetic_algorithm(N)
    except ValueError:
        print("Please enter a valid integer.")
