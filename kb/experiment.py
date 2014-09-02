import collections
import itertools
import random

from deap import base, creator, tools, algorithms

import actor
import keyboard


def n_wise(iterable, n):
    iterables = itertools.tee(iterable, n)
    for i in range(1, n):
        to_be_advanced = iterables[i]
        for _ in range(i):
            next(to_be_advanced, None)
    return zip(*iterables)


### INTERNAL Stuff ###

kb = keyboard.SixKey()
keys = sorted(kb.keys)
ac = actor.SingleFinger()
alphabet = 'abcdef'

text = ''.join(random.choice(alphabet) for _ in range(2**10))
corpus = collections.Counter(n_wise(text, 2))


### DEAP Stuff ###
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_layout", lambda: random.sample(range(len(alphabet)), len(alphabet)))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_layout)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", lambda l: (ac.evaluate(kb, l, alphabet, corpus),))
toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    import numpy
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof

if __name__ == "__main__":
    pop, log, hof = main()
    print("Best individual is: %s\nwith fitness: %s" % (hof[0], hof[0].fitness))

    import matplotlib.pyplot as plt
    gen, avg, min_, max_ = log.select("gen", "avg", "min", "max")
    plt.plot(gen, avg, label="average")
    plt.plot(gen, min_, label="minimum")
    plt.plot(gen, max_, label="maximum")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="lower right")
    plt.show()
