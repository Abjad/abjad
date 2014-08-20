# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class ItemSelectorCallback(AbjadValueObject):
    r'''A item selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_apply_to_each',
        '_item',
        )

    ### INITIALIZER ###

    def __init__(self, item=0, apply_to_each=True):
        assert isinstance(item, int)
        self._item = item
        self._apply_to_each = bool(apply_to_each)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates tuple `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(tuple)
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        if self.apply_to_each:
            for subexpr in expr:
                try:
                    subresult = subexpr.__getitem__(self.item)
                    if not isinstance(subresult, prototype):
                        subresult = select(subresult)
                    result.append(subresult)
                except IndexError:
                    pass
        else:
            try:
                subresult = select(expr.__getitem__(self.item))
                result.append(subresult)
            except IndexError:
                pass
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def apply_to_each(self):
        r'''Is true if item selector callback will be applied against the
        contents of each selection, rather than against the sequence of
        selections itself.

        Otherwise false.

        Returns boolean.
        '''
        return self._apply_to_each

    @property
    def item(self):
        r'''Gets item selector callback item.

        Returns integer.
        '''
        return self._item