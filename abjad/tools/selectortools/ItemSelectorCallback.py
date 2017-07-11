# -*- coding: utf-8 -*-
import collections
import numbers
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import inspect
from abjad.tools.topleveltools import select


class ItemSelectorCallback(AbjadValueObject):
    r'''Item selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

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

    def __call__(self, argument, rotation=None):
        r'''Gets item from `argument`.

        Returns item.
        '''
        import abjad
        assert isinstance(argument, collections.Iterable), repr(argument)
        if self.apply_to_each:
            result = []
            for item in argument:
                result_ = self._get_item(item)
                result.append(result_)
            result = tuple(result)
        else:
            result = self._get_item(argument)
        return result

    ### PRIVATE METHODS ###

    def _get_item(self, argument):
        result = argument.__getitem__(self.item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def apply_to_each(self):
        r'''Is true if item selector callback will be applied against the
        contents of each selection, rather than against the sequence of
        selections itself.

        Otherwise false.

        Returns true or false.
        '''
        return self._apply_to_each

    @property
    def item(self):
        r'''Gets item selector callback item.

        Returns integer.
        '''
        return self._item
