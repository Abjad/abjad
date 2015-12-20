# -*- coding: utf-8 -*-
import copy
import types
from abjad.tools.selectiontools.ContiguousSelection import ContiguousSelection


class SliceSelection(ContiguousSelection):
    r'''A time-contiguous selection of components all in the same parent.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> staff[:2]
            ContiguousSelection(Note("c'4"), Note("d'4"))

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    # TODO: assert all are contiguous components in same parent
    def __init__(self, music=None):
        music = self._coerce_music(music)
        ContiguousSelection.__init__(self, music=music)