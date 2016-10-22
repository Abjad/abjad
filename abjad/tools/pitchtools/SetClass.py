# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SetClass(AbjadValueObject):
    r'''Forte number.

    ..  container:: example

        **Example 1.**

        ::

            >>> set_class = pitchtools.SetClass(4, 9)

        ::

            >>> print(format(set_class))
            pitchtools.SetClass(
                cardinality=4,
                rank=9,
                )

    Object model of set-class identifiers established by Alan Forte.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_cardinality',
        '_rank',
        )

    ### INITIALIZER ###

    def __init__(self, cardinality=1, rank=1):
        cardinality = int(cardinality)
        assert 1 <= cardinality < 12, repr(cardinality)
        rank = int(rank)
        assert 1 <= rank, repr(rank)
        self._cardinality = cardinality
        self._rank = rank

    ### PUBLIC PROPERTIES ###

    @property
    def cardinality(self):
        r'''Gets cardinality of Forte number.

        ..  container:: example

            ::

                >>> set_class = pitchtools.SetClass(4, 9)
                >>> set_class.cardinality
                4

        Set to integer between 1 and 12, inclusive.
        '''
        return self._cardinality

    @property
    def rank(self):
        r'''Gets rank of Forte number.

        ..  container:: example

            ::

                >>> set_class = pitchtools.SetClass(4, 9)
                >>> set_class.rank
                9

        Set to positive integer.
        '''
        return self._rank