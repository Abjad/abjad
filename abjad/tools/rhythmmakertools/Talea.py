# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Talea(AbjadObject):
    '''Talea.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_counts',
        '_denominator',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        counts=(1,),
        denominator=16,
        ):
        counts = self._to_tuple(counts)
        assert isinstance(counts, tuple)
        assert all(isinstance(x, int) for x in counts)
        self._counts = counts
        assert mathtools.is_nonnegative_integer_power_of_two(denominator)
        self._denominator = denominator

    ### PRIVATE METHODS ###

    @staticmethod
    def _to_tuple(expr):
        if isinstance(expr, list):
            expr = tuple(expr)
        return expr

    ### PUBLIC PROPERTIES ###

    @property
    def counts(self):
        r'''Gets counts of talea.

        Returns tuple.
        '''
        return self._counts

    @property
    def denominator(self):
        r'''Gets denominator of talea.

        Returns nonnegative integer power of two.
        '''
        return self._denominator
