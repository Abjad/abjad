# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Infinity(AbjadValueObject):
    r'''Infinity.

    ..  container:: example

        All numbers compare less than infinity:

        ::

            >>> 9999999 < Infinity
            True

        ::

            >>> 2**38 < Infinity
            True

    ..  container:: example

        Infinity compares equal to itself:

        ::

            >>> Infinity == Infinity
            True

    ..  container:: example

        Negative infinity compares less than infinity:

        ::

            >>> NegativeInfinity < Infinity
            True
    
    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad starts.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_value',
        )

    ### INTIALIZER ###

    def __init__(self):
        self._value = float('infinity')

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is also infinity. Otherwise false.

        Returns true or false.
        '''
        return super(Infinity, self).__eq__(argument)

    def __float__(self):
        r'''Convert infinity to float.

        Returns float.
        '''
        return self._value

    def __ge__(self, argument):
        r'''Is true for all values of `argument`.

        Returns true.
        '''
        return self._value >= argument

    def __gt__(self, argument):
        r'''Is true for all noninfinite values of `argument`. Otherwise false.

        Returns true or false.
        '''
        return self._value > argument

    def __hash__(self):
        r'''Hashes infinity.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Infinity, self).__hash__()

    def __le__(self, argument):
        r'''Is true when `argument` is infinite. Otherwise false.

        Returns true or false.
        '''
        return self._value <= argument

    def __lt__(self, argument):
        r'''Is true for no values of `argument`.

        Returns true or false.
        '''
        return self._value < argument

    def __sub__(self, argument):
        r'''Subtracts `argument` from infinity.

        Returns infinity or 0 if `argument` is also infinity.
        '''
        if argument is self:
            return 0
        return self

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_text=type(self).__name__,
            storage_format_text=type(self).__name__,
            )
