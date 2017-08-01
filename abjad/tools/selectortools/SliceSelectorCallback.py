# -*- coding: utf-8 -*-
import collections
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools import select


class SliceSelectorCallback(AbjadValueObject):
    r'''Slice selector callback.

    ::

        >>> import abjad

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

    def __call__(self, argument, rotation=None):
        r'''Iterates tuple `argument`.

        ..  container:: example

            For examples:

            ::

                >>> string = r"c'4 \times 2/3 { d'8 r8 e'8 } r16 f'16 g'8 a'4"
                >>> staff = abjad.Staff(string)
                >>> show(staff) # doctest: +SKIP

        ..  container:: example

                >>> selector = abjad.select()
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
        assert isinstance(argument, collections.Iterable), repr(argument)
        prototype = (scoretools.Container, selectiontools.Selection)
        result = []
        if self.apply_to_each:
            for subexpr in argument:
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
                subresult = self._get_item(argument)
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

    def _get_item(self, argument):
        slice_ = slice(self.start, self.stop)
        result = argument.__getitem__(slice_)
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
