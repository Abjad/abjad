# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import select


class SliceSelectorCallback(AbjadObject):
    r'''A slice selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument',
        )

    ### INITIALIZER ###

    def __init__(self, argument):
        assert isinstance(argument, (int, slice))
        self._argument = argument

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.
        '''
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        for subexpr in expr:
            try:
                subresult = subexpr.__getitem__(self.argument)
                if not isinstance(subresult, prototype):
                    subresult = select(subresult)
                result.append(subresult)
            except IndexError:
                pass
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self):
        r'''Gets slice selector callback argument.

        Returns int or slice.
        '''
        return self._argument
