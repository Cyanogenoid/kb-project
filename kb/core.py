import abc
from collections import namedtuple


Key = namedtuple('Key', ['x', 'y'])


class Keyboard(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractproperty
    def keys(self):
        """ Return the keys of this keyboard.

        :returns: An iterable of keys

        """
        pass


class Actor(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def evaluate(self, keyboard, layout, corpus):
        """ Calculate how much effort the actor has to exert to type the corpus using the layout.

        :param keyboard: The keyboard the layout is applied to.
        :type keyboard: Keyboard
        :param layout: The layout function to be evaluated.
        :type layout: dict
        :param corpus: The corpus used for evaluation.
        :type corpus: iterable of strings
        :returns: A floating point value in range [0, +inf] where lower values indicate less effort

        """
        pass
