# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class SliceSelectorCallback(AbjadValueObject):
    r'''A slice selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_apply_to_each',
        '_argument',
        )

    ### INITIALIZER ###

    def __init__(self, argument=0, apply_to_each=True):
        assert isinstance(argument, (int, slice, tuple))
        if isinstance(argument, slice):
            argument = (argument.start, argument.stop)
        elif isinstance(argument, tuple):
            assert len(argument) == 2
            assert all(isinstance(x, (int, type(None))) for x in argument)
        self._argument = argument
        self._apply_to_each = bool(apply_to_each)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.
        '''
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        argument = self.argument
        if isinstance(argument, tuple):
            argument = slice(argument[0], argument[1])
        if self.apply_to_each:
            for subexpr in expr:
                try:
                    subresult = subexpr.__getitem__(argument)
                    if not isinstance(subresult, prototype):
                        subresult = select(subresult)
                    result.append(subresult)
                except IndexError:
                    pass
        else:
            try:
                subresult = select(expr.__getitem__(argument))
                if isinstance(argument, int):
                    result.append(subresult)
                else:
                    result.extend(subresult)
            except IndexError:
                pass
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def apply_to_each(self):
        r'''Is true if slice selector callback will be applied against the
        contents of each selection, rather than against the sequence of
        selections itself.

        Otherwise false.

        Returns boolean.
        '''
        return self._apply_to_each

    @property
    def argument(self):
        r'''Gets slice selector callback argument.

        Returns integer or slice.
        '''
        return self._argument