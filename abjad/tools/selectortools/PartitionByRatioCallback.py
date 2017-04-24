# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools


class PartitionByRatioCallback(AbjadValueObject):
    r'''Partition-by-ratio selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_ratio',
        )

    ### INITIALIZER ###

    def __init__(self, ratio=None):
        ratio = ratio or mathtools.Ratio((1,))
        ratio = mathtools.Ratio(ratio)
        self._ratio = ratio

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Calls ratio selector callback on `argument`.

        Returns tuple of selections.
        '''
        assert isinstance(argument, tuple), repr(argument)
        assert len(argument) == 1, repr(argument)
        assert isinstance(argument[0], selectiontools.Selection), repr(argument)
        selection = argument[0]
        counts = mathtools.partition_integer_by_ratio(
            len(selection),
            self.ratio,
            )
        selections = sequencetools.Sequence(selection).partition_by_counts(
            counts=counts,
            )
        selections = [selectiontools.Selection(_) for _ in selections]
        return tuple(selections)

    ### PUBLIC PROPERTIES ###

    @property
    def ratio(self):
        r'''Gets ratio.

        Returns ratio.
        '''
        return self._ratio
