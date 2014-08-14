import collections
import itertools
import random

import actor
import keyboard


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


kb = keyboard.SixKey()
ac = actor.SingleFinger()
alphabet = 'abcdef'

text = ''.join(random.choice(alphabet) for _ in range(2**10))
corpus = collections.Counter(pairwise(text))

keys = sorted(kb.keys)
layouts = set()
for permutation in itertools.permutations(alphabet):
    layout = dict(zip(permutation, keys))
    effort = ac.evaluate(kb, layout, corpus)

    pretty_layout = " ".join(sorted(layout, key=lambda c: layout[c]))
    layouts.add((effort, pretty_layout))
best = min(layouts)

print(corpus)
print()
print(best[1][:6])
print(best[1][6:])
print()
print(best[0])
