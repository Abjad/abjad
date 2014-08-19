# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class FlattenSelectorCallback(AbjadValueObject):
    r'''A flatten selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_depth',
        )

    ### INITIALIZER ###

    def __init__(self, depth=-1):
        self._depth = depth

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.

        ..  todo:: Does this always return a tuple of selections?
        '''
        assert isinstance(expr, tuple), repr(tuple)
        return sequencetools.flatten_sequence(
            expr, 
            depth=self.depth,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''Gets depth of callback.

        Returns integer.
        '''
        return self._depth