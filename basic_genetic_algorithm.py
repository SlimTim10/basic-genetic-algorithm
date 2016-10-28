# http://www.ai-junkie.com/ga/intro/gat3.html
# 
# Given the digits 0 through 9 and the operators +, -, * and /,  find a sequence that will represent a given target number. The operators will be applied sequentially from left to right as you read.
# So, given the target number 23, the sequence 6+5*4/2+1 would be one possible solution.

import random
import sys
import operator

character_list = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': '+',
    '1011': '-',
    '1100': '*',
    '1101': '/' }

target = 42
population = 300
chromosome_length = 50
crossover_rate = 0.7
mutation_rate = 0.001

random.seed(1)

class Chromosome:
    def __init__(self, body):
        self.body = body
        self.fitness = 0.0
        self.equation = ''
        self.result = 0.0

# Return n random chromosomes each of length chromo_length
def generate_random_chromosomes(n, chromo_length):
    chromos = []
    
    for i in range(n):
        tmp = ''
        for j in range(chromo_length):
            r = random.randint(0, len(character_list) - 1)
            tmp += list(character_list.keys())[r]
        chromos.append(Chromosome(tmp))
        
    return chromos

# Return the result of an equation (don't use operator precedence)
def get_result(equation):
    result = float(equation[0])
    i = 1
    while i < len(equation) - 1:
        n = int(equation[i + 1])
        if equation[i] == '+':
            result += n
        if equation[i] == '-':
            result -= n
        if equation[i] == '*':
            result *= n
        if equation[i] == '/':
            try:
                result /= n
            except:
                pass
        i += 2
    return result

# Return a randomly selected chromosome based on roulette wheel selection
def roulette_select(chromosomes, total_fitness):
    roll = random.random() * total_fitness
    f = 0.0
    for chromo in chromosomes:
        f += chromo.fitness
        if f > roll:
            return chromo
    return chromosomes[-1]

# Crossover two chromosomes based on crossover rate, and return them
def crossover(chromo1, chromo2):
    r = random.random()
    if r < crossover_rate:
        n = random.randint(0, chromosome_length - 1)
        tmp = chromo1.body
        chromo1.body = chromo1.body[0:n] + chromo2.body[n:]
        chromo2.body = chromo2.body[0:n] + tmp[n:]
    return chromo1, chromo2

# Mutate a chromosome based on mutation rate, and return the chromosome
def mutate(chromo):
    mutated = ''
    for i in range(0, chromosome_length):
        r = random.random()
        if r < mutation_rate:
            if chromo.body[i] == '0':
                mutated += '1'
            else:
                mutated += '0'
        else:
            mutate += chromo.body[i]
    chromo.body = mutated
    return chromo

chromosomes = generate_random_chromosomes(population, chromosome_length)

generation = 0
while True:
    
    total_fitness = 0.0
    
    for index, chromo in enumerate(chromosomes):
        # Split chromosome into character groups
        chars = [chromo.body[i:i+4] for i in range(0, len(chromo.body), 4)]
        prev_char = ''
        chromo.equation = ''

        for char in chars:
            try:
                char = character_list[char]
            except:
                char = ''
                # Alternate numbers and operators
            if prev_char.isdigit() != char.isdigit():
                chromo.equation += char
            else:
                continue
            prev_char = char

        # Don't let equations end with operator
        if not chromo.equation[-1].isdigit():
            chromo.equation = chromo.equation[:-1]

        chromo.result = 0
        try:
            chromo.result = get_result(chromo.equation)
        except:
            chromo.result = 0

        if int(chromo.result) == target:
            print('Found a solution!')
            print('Chromosome {0}: {1}'.format(index, chromo.body))
            print('Equation:', chromo.equation)
            print('Result:', chromo.result)
            print('Fitness score:', chromo.fitness)
            sys.exit(0)

        chromo.fitness = abs(1.0 / (target - chromo.result))
        total_fitness += chromo.fitness

    if generation % 100 == 0:
        # Find best chromosome
        best_chromo = sorted(chromosomes, key=operator.attrgetter('fitness'), reverse=True)[0]
        print('Generation:', generation)
        print('Best chromosome:', best_chromo.body)
        print('Equation:', best_chromo.equation)
        print('Result:', best_chromo.result)
        print('Fitness score:', best_chromo.fitness)
        print()

    pop = 0
    while pop < population:
        offspring1 = roulette_select(chromosomes, total_fitness)
        offspring2 = roulette_select(chromosomes, total_fitness)

        offspring1, offspring2 = crossover(offspring1, offspring2)

        chromosomes[pop] = offspring1
        pop += 1
        chromosomes[pop] = offspring2
        pop += 1
    
    generation += 1
