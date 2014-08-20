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
        '_start',
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(self, start=None, stop=None, apply_to_each=True):
        assert isinstance(start, (int, type(None)))
        assert isinstance(stop, (int, type(None)))
        self._start = start
        self._stop = stop
        self._apply_to_each = bool(apply_to_each)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(tuple)
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        argument = slice(self.start, self.stop)
        if self.apply_to_each:
            for subexpr in expr:
                try:
                    subresult = subexpr.__getitem__(argument)
                    if not isinstance(subresult, prototype):
                        subresult = select(subresult)
                    if isinstance(subresult, selectiontools.Selection):
                        if subresult:
                            result.append(subresult)
                    else:
                        result.append(subresult)
                except IndexError:
                    pass
        else:
            try:
                subresult = select(expr.__getitem__(argument))
                if isinstance(subresult, selectiontools.Selection):
                    if subresult:
                        result.extend(subresult)
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
    def start(self):
        r'''Gets slice selector callback start.

        Returns integer.
        '''
        return self._start

    @property
    def stop(self):
        r'''Gets slice selector callback stop.

        Returns integer.
        '''
        return self._stop