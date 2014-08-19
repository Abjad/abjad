# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class MeasureSelectorCallback(AbjadValueObject):
    r'''A measure selector callback.

    Groups components by start measure.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.

        Returns tuple of selections.
        '''
        # TODO:
        pass