# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class SliceSelectorCallback(AbjadValueObject):
    r'''A slice selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

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

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        ..  container:: example

            For examples:

            ::

                >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
                >>> staff = Staff(string)
                >>> show(staff) # doctest: +SKIP

        ..  container:: example

            **Example 1.**

                >>> selector = selectortools.Selector()
                >>> selector = selector.get_slice(start=-4)
                >>> selections = selector(staff)

            ::

                >>> for selection in selections:
                ...     selection
                ...
                Selection([Rest('r16'), Note("f'16"), Note("g'8"), Note("a'4")])

            Returns tuple of selections.

        Returns tuple of selections or tuple of selections with offset.
        '''
        assert isinstance(expr, tuple), repr(expr)
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        if self.apply_to_each:
            for subexpr in expr:
                try:
                    subresult = self._get_item(subexpr)
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
                subresult = self._get_item(expr)
                subresult = select(subresult)
                if isinstance(subresult, selectiontools.Selection):
                    if subresult:
                        result.extend(subresult)
                else:
                    result.extend(subresult)
            except IndexError:
                pass
        return tuple(result)

    ### PRIVATE METHODS ###

    def _get_item(self, expr):
        slice_ = slice(self.start, self.stop)
        result = expr.__getitem__(slice_)
        return result

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
