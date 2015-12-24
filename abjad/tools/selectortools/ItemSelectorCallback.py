# -*- coding: utf-8 -*-
import numbers
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import select


class ItemSelectorCallback(AbjadValueObject):
    r'''An item selector callback.
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

    def __call__(self, expr, start_offset=None):
        r'''Gets item from `expr`.

        Returns item.
        '''
        assert isinstance(expr, tuple), repr(expr)
        if self.apply_to_each:
            result = []
            for element in expr:
                result_ = self._get_item(element, start_offset)
                result_, new_start_offset = result_
                result.append(result_)
            result = tuple(result)
        else:
            result = self._get_item(expr, start_offset)
            result, new_start_offset = result
        return result, new_start_offset

    ### PRIVATE METHODS ###

    def _get_item(self, expr, start_offset=None):
        result = expr.__getitem__(self.item)
        new_start_offset = start_offset
        if new_start_offset is not None:
            preceding_items = expr[:self.item]
            for item in preceding_items:
                if isinstance(item, numbers.Number):
                    new_start_offset += item
                    continue
                if hasattr(item, 'duration'):
                    duration = item.duration
                    new_start_offset += duration
                    continue
                if hasattr(item, 'get_duration'):
                    duration = item.get_duration()
                    new_start_offset += duration
                    continue
                try:
                    duration = inspect_(item).get_duration()
                    new_start_offset += duration
                except AssertionError:
                    pass
            new_start_offset = durationtools.Offset(new_start_offset)
        return result, new_start_offset

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