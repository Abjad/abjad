from abjad.tools.abctools import AbjadObject


class Infinity(AbjadObject):
    '''Object-oriented infinity.

    All numbers compare less than infinity:

    ::

        >>> 9999999 < Infinity
        True

    ::

        >>> 2**38 < Infinity
        True

    Infinity compares equal to itself:

    ::

        >>> Infinity == Infinity
        True

    Negative infinity compares less than infinity:

    ::

        >>> NegativeInfinity < Infinity
        True

    Infinity is initialized at start-up and is available in the global Abjad namespace.
    '''

    ### INTIALIZER ###

    def __init__(self):
        self._value = float('infinity')

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            return self._value == expr._value
        return False

    def __ge__(self, expr):
        return self._value >= expr

    def __gt__(self, expr):
        return self._value > expr

    def __le__(self, expr):
        return self._value <= expr

    def __lt__(self, expr):
        return self._value < expr

    def __repr__(self):
        return self._class_name
