import abc
from decimal import Decimal

from core import Key, Keyboard


class StandardKeyboard(Keyboard):
    """ A StandardKeyboard is a keyboard with standard Cherry MX key sizes and spacings. (see: http://www.fentek-ind.com/images/CHERRY_MX_keyswitch.pdf)

    """
    def __init__(self):
        self.unit_height = Decimal('19.05')
        self.unit_width = Decimal('19.05')
        self.separator = '|'
        self.comment = '-'
        self.padding = 'x'
        self._keys = None


    @property
    def keys(self):
        if self._keys == None:
            self._keys = self.load_schema()
        return self._keys


    def load_schema(self):
        keys = list()
        offset_y = Decimal(0)
        for line in self.schema.splitlines():
            # don't process lines starting with the comment prefix
            if line.startswith(self.comment):
                continue
            offset_x = Decimal(0)
            for key in line.strip(self.separator).split(self.separator):
                # only add the key if it isn't padding
                if self.padding not in key:
                    keys.append(Key(x=offset_x, y=offset_y))
                unit = Decimal(len(key) * 0.25 + 1)
                offset_x += Decimal(self.unit_width * unit)
            offset_y += Decimal(self.unit_height)
        return keys


    @abc.abstractproperty
    def schema(self):
        pass


class ANSI(StandardKeyboard):
    def __init__(self):
        super().__init__()

    @property
    def schema(self):
        return """\
-------------------------------------------------------------
|   |   |   |   |   |   |   |   |   |   |   |   |   |       |
-------------------------------------------------------------
|     |   |   |   |   |   |   |   |   |   |   |   |   |     |
-------------------------------------------------------------
|      |   |   |   |   |   |   |   |   |   |   |   |        |
-------------------------------------------------------------
|        |   |   |   |   |   |   |   |   |   |   |          |
-------------------------------------------------------------
|    |    |    |                        |    |    |    |    |
-------------------------------------------------------------
        """


class Core33(StandardKeyboard):
    def __init__(self):
        super().__init__()

    @property
    def schema(self):
        return """\
-------------------------------------------------------------
|  x  |   |   |   |   |   |   |   |   |   |   |   |   |  x  |
-------------------------------------------------------------
|   x  |   |   |   |   |   |   |   |   |   |   |   |    x   |
-------------------------------------------------------------
|     x  |   |   |   |   |   |   |   |   |   |   |    x     |
-------------------------------------------------------------
        """


class SixKey(StandardKeyboard):
    def __init__(self):
        super().__init__()

    @property
    def schema(self):
        return """\
-------------
|   |   |   |
-------------
|   |   |   |
-------------
        """
