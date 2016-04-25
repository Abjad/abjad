# -*- coding: utf-8 -*-
from abjad.tools.mathtools.Infinity import Infinity


class NegativeInfinity(Infinity):
    r'''Object-oriented negative infinity.

    All numbers compare greater than negative infinity:

    ::

        >>> NegativeInfinity < -9999999
        True

    Negative infinity compares equal to itself:

    ::

        >>> NegativeInfinity == NegativeInfinity
        True

    Negative infinity compares less than infinity:

    ::

        >>> NegativeInfinity < Infinity
        True

    Negative infinity is initialize at start-up and is available in the
    global Abjad namespace.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        self._value = float('-infinity')
