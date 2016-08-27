# -*- coding: utf-8 -*-
from abjad.tools import systemtools
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

    ### CLASS VARIABLES ###

    __slots__ = (
        '_value',
        )

    ### INTIALIZER ###

    def __init__(self):
        self._value = float('infinity')

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is also infinity. Otherwise false.

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self._value == expr._value
        return False

    def __ge__(self, expr):
        r''' True for all values of `expr`. Otherwise false.

        Returns true or false.
        '''
        return self._value >= expr

    def __gt__(self, expr):
        r'''True for all noninfinite values of `expr`. Otherwise false.

        Returns true or false.
        '''
        return self._value > expr

    def __hash__(self):
        r'''Hashes infinity.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Infinity, self).__hash__()

    def __le__(self, expr):
        r'''Is true when `expr` is infinite. Otherwise false.

        Returns true or false.
        '''
        return self._value <= expr

    def __lt__(self, expr):
        r'''True for no values of `expr`.

        Returns true or false.
        '''
        return self._value < expr

    def __sub__(self, expr):
        r'''Subtracts `expr` from infinity.

        Returns infinity or 0 if `expr` is also infinity.
        '''
        if expr is self:
            return 0
        return self

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_text=type(self).__name__,
            storage_format_text=type(self).__name__,
            )
