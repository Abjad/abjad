# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Infinity(AbjadObject):
    r'''Object-oriented infinity.

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

    Infinity is initialized at start-up and is available in the 
    global Abjad namespace.
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

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        return self._storage_format_specification

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            storage_format_pieces=(
                type(self).__name__,
                ),
            )
