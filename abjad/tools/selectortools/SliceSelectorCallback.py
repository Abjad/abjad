# -*- coding: utf-8 -*-
import numbers
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import inspect_
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

    def __call__(self, expr, start_offset=None):
        r'''Iterates tuple `expr`.

        ..  container:: example

            For examples:

            ::

                >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
                >>> staff = Staff(string)
                >>> show(staff) # doctest: +SKIP

        ..  container:: example

            **Example 1.** When start offset is none:

                >>> selector = selectortools.Selector()
                >>> selector = selector.get_slice(start=-4)
                >>> selections = selector(staff)

            ::

                >>> for selection in selections:
                ...     selection
                ContiguousSelection(Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4"))

            Returns tuple of selections.

        ..  container:: example

            **Example 2.** When start offset is not none:

                >>> selector = selectortools.Selector()
                >>> selector = selector.get_slice(start=-4)
                >>> result = selector(staff, start_offset=Offset(0))
                >>> selections, start_offset = result

            ::

                >>> for selection in selections:
                ...     selection
                ContiguousSelection(Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4"))

            ::

                >>> start_offset
                Offset(1, 2)

            Returns tuple of selections together with start offset of
            selection.

            Selection starts at offset 1/2 (from start of input expression).

        ..  container:: example

            **Example 3.** When start offset is not none, again:

                >>> selector = selectortools.Selector()
                >>> selector = selector.get_slice(start=-3)
                >>> result = selector(staff, start_offset=Offset(0))
                >>> selections, start_offset = result

            ::

                >>> for selection in selections:
                ...     selection
                ContiguousSelection(Note("f'16"), Note("g'8"), Note("a'4"))

            ::

                >>> start_offset
                Offset(9, 16)

            Selection starts at offset 9/16 (from start of input expression).

        Returns tuple of selections or tuple of selections with offset.
        '''
        assert isinstance(expr, tuple), repr(tuple)
        new_start_offset = start_offset
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        slice_ = slice(self.start, self.stop)
        if self.apply_to_each:
            for subexpr in expr:
                try:
                    #subresult = subexpr.__getitem__(slice_)
                    subresult, new_start_offset = self._get_item(
                        subexpr, 
                        start_offset,
                        )
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
                #subresult = select(expr.__getitem__(slice_))
                #subresult = select(self._get_item(expr, start_offset))
                subresult, new_start_offset = self._get_item(
                    expr, 
                    start_offset,
                    )
                subresult = select(subresult)
                if isinstance(subresult, selectiontools.Selection):
                    if subresult:
                        result.extend(subresult)
                else:
                    result.extend(subresult)
            except IndexError:
                pass
        return tuple(result), new_start_offset

    ### PRIVATE METHODS ###

    def _get_item(self, expr, start_offset=None):
        slice_ = slice(self.start, self.stop)
        result = expr.__getitem__(slice_)
        start, stop, stride = slice_.indices(len(expr))
        new_start_offset = start_offset
        if new_start_offset is not None:
            preceding_items = expr[:start]
            for item in preceding_items:
                if isinstance(item, numbers.Number):
                    new_start_offset += item
                    continue
                if hasattr(item, 'duration'):
                    duration = item.duration
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
        r'''Is true if slice selector callback will be applied against the
        contents of each selection, rather than against the sequence of
        selections itself.

        Otherwise false.

        Returns true or false.
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