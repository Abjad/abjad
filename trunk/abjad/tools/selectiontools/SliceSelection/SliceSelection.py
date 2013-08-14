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
        #from abjad.tools import componenttools
        music = self._coerce_music(music)
        #assert componenttools.all_are_contiguous_components_in_same_parent(
        #    music), repr(music)
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

    ### PUBLIC METHODS ###

    def replace_with_rests(
        self,
        decrease_durations_monotonically=True,
        ):
        r'''Replace components in selection with one or more rests.

        **Example 1.** Replace all container elements:

        ..  container:: example

            ::

                >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                \new Staff {
                    c'8
                    d'8
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    c''8
                }

            ::

                >>> container[:].replace_with_rests()
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                \new Staff {
                    r1
                }

        **Example 2.** Replace container elements from ``1`` forward:

        ..  container:: example

            ::

                >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")
                >>> show(container) # doctest: +SKIP

            ::

                >>> container[1:].replace_with_rests()
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                \new Staff {
                    c'8
                    r2..
                }

        **Example 3.** Replace container elements from ``1`` to ``2``:

        ..  container:: example

            ::

                >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")
                >>> show(container) # doctest: +SKIP

            ::

                >>> container[1:2].replace_with_rests()
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                \new Staff {
                    c'8
                    r8
                    e'8
                    f'8
                    g'8
                    a'8
                    b'8
                    c''8
                }

        Return none.
        '''
        from abjad.tools import resttools
        assert self._all_are_contiguous_components_in_same_parent(self)
        if self:
            duration = self._preprolated_duration
            rests = resttools.make_rests(
                duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                )
            parent, start, stop = self._get_parent_and_start_stop_indices()
            parent[start:stop+1] = rests
