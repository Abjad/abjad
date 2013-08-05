# -*- encoding: utf-8 -*-
import copy
import itertools
import types
from abjad.tools.selectiontools.Selection import Selection


class SliceSelection(Selection):
    r'''Selection of components sliced from a sequential container.

    **Example**:

    ..  container:: example

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

    def __init__(self, music=None):
        if music is None:
            music = ()
        elif isinstance(music, (tuple, list)):
            music = tuple(music)
        elif isinstance(music, Selection):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Add `expr` to slice selection.

        Return new slice selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = self._music + expr._music
            return type(self)(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        return type(self)(music)

    def __radd__(self, expr):
        '''Add slice selection to `expr`.

        Return new slice selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr._music + self._music
            return type(self)(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self._music
        return SliceSelection(music)

    ### PRIVATE PROPERTIES ###

    @property
    def _preprolated_duration(self):
        return sum(component._preprolated_duration for component in self)

    ### PRIVATE METHODS ###

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component.get_timespan().start_offset)
            stop_offsets.append(component.get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _get_parent_and_start_stop_indices(self):
        if self:
            first, last = self[0], self[-1]
            parent = first._parent
            if parent is not None:
                first_index = parent.index(first)
                last_index = parent.index(last)
                return parent, first_index, last_index
        return None, None, None

    def _give_dominant_spanners_to_components(self, recipients):
        r'''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Return none.
        Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        assert componenttools.all_are_thread_contiguous_components(recipients)
        receipt = spannertools.get_spanners_that_dominate_components(self)
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _give_music_to_empty_container(self, container):
        r'''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
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
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
        assert isinstance(container, containertools.Container)
        parent, start, stop = self._get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

    def _set_parents(self, new_parent):
        r'''Not composer-safe.
        '''
        for component in self._music:
            component._set_parent(new_parent)

    def _withdraw_from_crossing_spanners(self):
        r'''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        crossing_spanners = \
            spannertools.get_spanners_that_cross_components(self)
        components_including_children = \
            list(iterationtools.iterate_components_in_expr(self))
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner._components[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._components.remove(component)
                    component._spanners.discard(crossing_spanner)

    ### PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        r'''Timespan of slice selection.

        Return timespan.
        '''
        from abjad.tools import timespantools
        start_offset = min(x.get_timespan().start_offset for x in self)
        stop_offset = max(x.get_timespan().stop_offset for x in self)
        return timespantools.Timespan(start_offset, stop_offset)

    ### PUBLIC METHODS ###

    def get_duration(self, in_seconds=False):
        r'''Get duration of components in selection.

        Return duration.
        '''
        return sum(
            component.get_duration(in_seconds=in_seconds) 
            for component in self
            )

    def group_by(self, predicate):
        '''Group components in selection by `predicate`.

        Return list of tuples.
        '''
        result = []
        grouper = itertools.groupby(self, predicate)
        for label, generator in grouper:
            #selection = type(self)(generator)
            selection = tuple(generator)
            result.append(selection)
        return result

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
        if self:
            duration = self._preprolated_duration
            rests = resttools.make_rests(
                duration,
                decrease_durations_monotonically=decrease_durations_monotonically,
                )
            parent, start, stop = self._get_parent_and_start_stop_indices()
            parent[start:stop+1] = rests
