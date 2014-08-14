# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import select


class PrototypeSelectorCallback(AbjadValueObject):
    r'''A prototype selector callback.
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
            subresult = iterate(subexpr).by_class(prototype)
            subresult = select(subresult)
            if subresult:
                result.append(subresult)
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets prototype selector callback prototype.

        Return tuple of classes.
        '''
        return self._prototype