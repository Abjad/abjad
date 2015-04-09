# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadValueObject


class FlattenDivisionCallback(AbjadValueObject):
    r'''Flatten division callback.
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
        r'''Calls flatten division callback on `expr`.

        Returns list of divisions or list of division lists.
        '''
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