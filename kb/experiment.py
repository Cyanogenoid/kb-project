import collections
import itertools
import random

from deap import base, creator, tools, algorithms
from nltk.corpus import brown

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

kb = keyboard.Core33()
keys = sorted(kb.keys)
ac = actor.SingleFinger()
alphabet = "abcdefghijklmnopqrstuvwxyz"

alphabet_set = set(alphabet)

print('Processing corpus...')
text = itertools.chain.from_iterable(map(str.lower, brown.words()))
corpus = collections.Counter(n_wise(filter(lambda c: c in alphabet_set, text), 3))


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
toolbox.register("select", tools.selTournament, tournsize=6)


def show_individual(individual):
    font_size = 14

    max_x = max(keys[i].x for i in individual)
    max_y = max(keys[i].y for i in individual)

    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGBA', (max_x + 2*font_size, max_y + 2*font_size))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("DejaVuSans.ttf", font_size)

    for i, c in enumerate(alphabet):
        key = keys[individual[i]]
        target_position = (key.x, key.y)
        draw.text(target_position, c, fill=(0, 0, 0), font=font)

    image.save('layout.png')


def main():
    import numpy
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=200, stats=stats, halloffame=hof, verbose=True)

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
    plt.ylabel("Effort")
    plt.legend(loc="upper right")
    plt.show()
    show_individual(hof[0])
