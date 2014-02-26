# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadObject
from abjad.tools import selectiontools
from abjad.tools.topleveltools import iterate


class RunSelectorCallback(AbjadObject):
    r'''A run selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_prototype',
        )

    ### INITIALIZER ###

    def __init__(self, prototype):
        if isinstance(prototype, collections.Sequence):
            prototype = tuple(prototype)
            assert all(isinstance(x, type) for x in prototype)
        assert isinstance(prototype, (tuple, type))
        self._prototype = prototype

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.
        '''
        result = []
        prototype = self.prototype
        if not isinstance(prototype, tuple):
            prototype = (prototype,)
        for subexpr in expr:
            for run in iterate(subexpr).by_run(prototype):
                run = selectiontools.Selection(run)
                result.append(run)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets run selector callback prototype.

        Return tuple of classes.
        '''
        return self._prototype
