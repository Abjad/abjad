# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools


class PartitionByRatioCallback(AbjadValueObject):
    r'''A ratio selector callback.
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

    def __call__(self, expr, start_offset=None):
        r'''Calls ratio selector callback on `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(expr)
        assert len(expr) == 1, repr(expr)
        assert isinstance(expr[0], selectiontools.Selection), repr(expr)
        new_start_offset = start_offset
        selection = expr[0]
        counts = mathtools.partition_integer_by_ratio(
            len(selection), 
            self.ratio,
            )
        selections = sequencetools.partition_sequence_by_counts(
            selection,
            counts=counts,
            )
        return tuple(selections), new_start_offset

    ### PUBLIC PROPERTIES ###

    @property
    def ratio(self):
        r'''Gets ratio.

        Returns ratio.
        '''
        return self._ratio