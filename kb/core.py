import abc
from collections import namedtuple


Key = namedtuple('Key', ['x', 'y'])


class Keyboard(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractproperty
    def keys(self):
        pass
