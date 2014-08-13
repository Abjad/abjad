# -*- encoding: utf-8 -*-
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class FlattenSelectorCallback(AbjadValueObject):
    r'''A flatten selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.
        '''
        return (
            selectiontools.Selection(
                sequencetools.flatten_sequence(expr)),
            )
