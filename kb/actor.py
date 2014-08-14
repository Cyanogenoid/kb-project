import math

from core import Actor


class SingleFinger(Actor):
    def evaluate(self, keyboard, layout, corpus):
        # start out with no effort
        effort = 0.0
        # process corpus
        for n_gram, weight in corpus.items():
            # use partial effort to apply weight to
            partial_effort = 0.0
            # reset x and y position of finger before starting
            x, y = None, None
            # try to type out all characters
            for character in n_gram:
                try:
                    target = layout[character]
                except KeyError:
                    # corpus can't be typed out with layout
                    return float('+inf')
                if x != None and y != None:
                    # squared distance between current finger position to target position
                    distance = (x - target.x)**2 + (y - target.y)**2
                else:
                    distance = 0.0
                partial_effort += float(distance)
                # move current finger position to target position
                x, y = target.x, target.y
            # add with weighting to effort
            effort += partial_effort * weight
        return effort
