# -*- encoding: utf-8 -*-
import copy
import types
from abjad.tools.selectiontools.ContiguousSelection import ContiguousSelection


class SliceSelection(ContiguousSelection):
    r'''A time-contiguous selection of components all in the same parent.

    ..  container:: example

        **Example.**

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> staff[:2]
            SliceSelection(Note("c'4"), Note("d'4"))

    '''

    ### INITIALIZER ###

    # TODO: assert all are contiguous components in same parent
    def __init__(self, music=None):
        music = self._coerce_music(music)
        ContiguousSelection.__init__(self, music=music)

    ### PRIVATE METHODS ###

    def _get_parent_and_start_stop_indices(self):
        assert self._all_are_contiguous_components_in_same_parent(self)
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _give_music_to_empty_container(self, container):
        r'''Not composer-safe.
        '''
        from abjad.tools import containertools
        assert self._all_are_contiguous_components_in_same_parent(self)
        assert isinstance(container, containertools.Container)
        assert not container
        music = []
        for component in self:
            music.extend(getattr(component, '_music', ()))
        container._music.extend(music)
        container[:]._set_parents(container)

    def _give_position_in_parent_to_container(self, container):
        r'''Not composer-safe.
        '''
        from abjad.tools import containertools
        assert self._all_are_contiguous_components_in_same_parent(self)
        assert isinstance(container, containertools.Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)
