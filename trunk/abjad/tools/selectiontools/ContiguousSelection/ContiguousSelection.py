# -*- encoding: utf-8 -*-
import copy
import itertools
import types
from abjad.tools.selectiontools.Selection import Selection


class ContiguousSelection(Selection):
    r'''A time-contiguous selection of components.
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
        from abjad.tools import componenttools
        from abjad.tools import selectiontools
        assert isinstance(expr, (Selection, list, tuple))
        if isinstance(expr, type(self)):
            music = self._music + expr._music
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        if componenttools.all_are_contiguous_components_in_same_logical_voice(music):
            return type(self)(music)
        else:
            return selectiontools.FreeComponentSelection(music) 

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
        return ContiguousSelection(music)

    ### PRIVATE PROPERTIES ###

    @property
    def _preprolated_duration(self):
        return sum(component._preprolated_duration for component in self)

    ### PRIVATE METHODS ###

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component._get_timespan().start_offset)
            stop_offsets.append(component._get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _give_dominant_spanners_to_components(self, recipients):
        r'''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Return none.
        Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        assert componenttools.all_are_contiguous_components_in_same_logical_voice(self)
        assert componenttools.all_are_contiguous_components_in_same_logical_voice(recipients)
        receipt = spannertools.get_spanners_that_dominate_components(self)
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

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
        assert componenttools.all_are_contiguous_components_in_same_logical_voice(self)
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

    ### PUBLIC METHODS ###

    def copy_and_fracture_crossing_spanners(self, n=1):
        r'''Copies components in selection and fractures crossing spanners.

        Components in selection must be logical-voice-contiguous.

        The steps this function takes are as follows:

            * Deep copy `components`.

            * Deep copy spanners that attach to any component in `components`.

            * Fracture spanners that attach to components not in `components`.

            * Return Python list of copied components.

        ..  container:: example

            **Example 1.** Copy components one time:

            ::

                >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
                >>> staff.append(r"g'8 a'8 b'8 c''8")
                >>> time_signature = contexttools.TimeSignatureMark((2, 4))
                >>> time_signature = time_signature.attach(staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest:: 
            
                >>> f(staff)
                \new Staff {
                    \time 2/4
                    c'8 (
                    d'8
                    e'8
                    f'8 )
                    g'8
                    a'8
                    b'8
                    c''8
                }

            ::

                >>> selection = staff.select_leaves()[2:4]
                >>> result = selection.copy_and_fracture_crossing_spanners()
                >>> new_staff = Staff(result)
                >>> show(new_staff) # doctest: +SKIP

            ..  doctest::

                >>> f(new_staff)
                \new Staff {
                    e'8 (
                    f'8 )
                }

            ::

                >>> staff.select_leaves()[2] is new_staff.select_leaves()[0]
                False

        ..  container:: example

            **Example 2.** Copy components multiple times:

            Copy `components` a total of `n` times:
            
            ::

                >>> selection = staff.select_leaves()[2:4]
                >>> result = selection.copy_and_fracture_crossing_spanners(n=4)
                >>> new_staff = Staff(result)
                >>> show(new_staff) # doctest: +SKIP

            ::

                >>> f(new_staff)
                \new Staff {
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                    e'8 (
                    f'8 )
                }

        Returns contiguous selection.
        '''
        from abjad.tools import spannertools
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        # check input
        assert self._all_are_logical_voice_contiguous_components()
        # return empty list when nothing to copy
        if n < 1:
            return []
        new_components = [
            component._copy_with_children_and_marks_but_without_spanners() 
            for component in self
            ]
        new_components = type(self)(new_components)
        # make schema of spanners contained by components
        schema = spannertools.make_spanner_schema(self)
        # copy spanners covered by components
        for covered_spanner, component_indices in schema.items():
            new_covered_spanner = copy.copy(covered_spanner)
            del(schema[covered_spanner])
            schema[new_covered_spanner] = component_indices
        # reverse schema
        reversed_schema = {}
        for new_covered_spanner, component_indices in schema.items():
            for component_index in component_indices:
                try:
                    reversed_schema[component_index].append(new_covered_spanner)
                except KeyError:
                    reversed_schema[component_index] = [new_covered_spanner]
        # iterate components and add new components to new spanners
        for component_index, new_component in enumerate(
            iterationtools.iterate_components_in_expr(new_components)):
            try:
                new_covered_spanners = reversed_schema[component_index]
                for new_covered_spanner in new_covered_spanners:
                    new_covered_spanner.append(new_component)
            except KeyError:
                pass
        # repeat as specified by input
        for i in range(n - 1):
            new_components += self.copy_and_fracture_crossing_spanners()
        # return new components
        return new_components
            
    def get_duration(self, in_seconds=False):
        r'''Gets duration of contiguous selection.

        Returns duration.
        '''
        return sum(
            component._get_duration(in_seconds=in_seconds) 
            for component in self
            )

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of contiguous selection.

        Returns timespan.
        '''
        from abjad.tools import timespantools
        if in_seconds:
            raise NotImplementedError
        start_offset = min(x._get_timespan().start_offset for x in self)
        stop_offset = max(x._get_timespan().stop_offset for x in self)
        return timespantools.Timespan(start_offset, stop_offset)

    def group_by(self, predicate):
        '''Groups components in contiguous selection by `predicate`.

        Returns list of tuples.
        '''
        result = []
        grouper = itertools.groupby(self, predicate)
        for label, generator in grouper:
            selection = tuple(generator)
            result.append(selection)
        return result
