# -*- encoding: utf-8 -*-
import copy
import itertools
import types
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.selectiontools.Selection import Selection


class ContiguousSelection(Selection):
    r'''A time-contiguous selection of components.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        music = self._coerce_music(music)
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
        if self._all_are_contiguous_components_in_same_logical_voice(music):
            return type(self)(music)
        else:
            return selectiontools.Selection(music) 

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
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        assert self._all_are_contiguous_components_in_same_logical_voice(recipients)
        receipt = spannertools.get_spanners_that_dominate_components(self)
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _withdraw_from_crossing_spanners(self):
        r'''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import spannertools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
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

    def _copy(self, n=1, include_enclosing_containers=False):
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
                >>> result = selection._copy()
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
                >>> result = selection._copy(n=4)
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

        ..  container:: example

            **Example 3.** Copy leaves and include enclosing conatiners:

                >>> voice = Voice(r"\times 2/3 { c'4 d'4 e'4 }")
                >>> voice.append(r"\times 2/3 { f'4 e'4 d'4 }")
                >>> staff = Staff([voice])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \new Voice {
                        \times 2/3 {
                            c'4
                            d'4
                            e'4
                        }
                        \times 2/3 {
                            f'4
                            e'4
                            d'4
                        }
                    }
                }

            ::

                >>> leaves = staff.select_leaves(1, 5)
                >>> new_staff = leaves._copy(include_enclosing_containers=True)
                >>> show(new_staff) # doctest: +SKIP

            ..  doctest::

                >>> f(new_staff)
                \new Staff {
                    \new Voice {
                        \times 2/3 {
                            d'4
                            e'4
                        }
                        \times 2/3 {
                            f'4
                            e'4
                        }
                    }
                }

        Returns contiguous selection.
        '''
        from abjad.tools import spannertools
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        # check input
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        # return empty list when nothing to copy
        if n < 1:
            return []
        new_components = [
            component._copy_with_children_and_marks_but_without_spanners() 
            for component in self
            ]
        if include_enclosing_containers:
            return self._copy_and_include_enclosing_containers()
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
            new_components += self._copy()
        # return new components
        return new_components

    def fuse_tuplets(self):
        r'''Fuse parent-contiguous tuplets in selection.

        ..  container:: example
        
            **Example.** Fuse parent-contiguous fxed-duration tuplets
            in selection:

            ::

                >>> t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), [])
                >>> t1.extend("c'8 d'8 e'8")
                >>> beam = spannertools.BeamSpanner(t1[:])
                >>> t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), [])
                >>> t2.extend("c'16 d'16 e'16")
                >>> slur = spannertools.SlurSpanner(t2[:])
                >>> staff = Staff([t1, t2])

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                    }
                    \times 2/3 {
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            ::

                >>> show(staff) # doctest: +SKIP

            ::

                >>> tuplets = staff[:]
                >>> tuplets.fuse_tuplets()
                FixedDurationTuplet(3/8, [c'8, d'8, e'8, c'16, d'16, e'16])

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            ::

                >>> show(staff) # doctest: +SKIP

        Return new tuplet.

        Fuse zero or more parent-contiguous `tuplets`.

        Allow in-score `tuplets`.

        Allow outside-of-score `tuplets`.

        All `tuplets` must carry the same multiplier.

        All `tuplets` must be of the same type.
        '''
        from abjad.tools import containertools
        from abjad.tools import tuplettools
        assert self._all_are_contiguous_components_in_same_parent(
            self, component_classes=(tuplettools.Tuplet,))
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                raise TupletFuseError('tuplets must carry same multiplier.')
            if type(tuplet) != first_type:
                raise TupletFuseError('tuplets must be same type.')
        if isinstance(first, tuplettools.FixedDurationTuplet):
            total_contents_duration = sum(
                [x._contents_duration for x in self])
            new_target_duration = first_multiplier * total_contents_duration
            new_tuplet = tuplettools.FixedDurationTuplet(
                new_target_duration, [])
        elif isinstance(first, tuplettools.Tuplet):
            new_tuplet = tuplettools.Tuplet(first_multiplier, [])
        else:
            raise TypeError('unknown tuplet type.')
        wrapped = False
        if self[0]._get_parentage().root is not \
            self[-1]._get_parentage().root:
            dummy_container = containertools.Container(self)
            wrapped = True
        containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
            self, new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet
            
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

    def partition_by_durations(
        self,
        durations,
        cyclic=False,
        fill='exact',
        in_seconds=False,
        overhang=False,
        ):
        r'''Partitions `components` according to `durations`.

        When `fill` is ``'exact'`` then parts must equal `durations` exactly.

        When `fill` is ``'less'`` then parts must be 
        less than or equal to `durations`.

        When `fill` is ``'greater'`` then parts must be 
        greater or equal to `durations`.

        Reads `durations` cyclically when `cyclic` is true.

        Reads component durations in seconds when `in_seconds` is true.

        Returns remaining components at end in final part when `overhang` 
        is true.
        '''
        # TODO: decide on correct assertion
        #assert self._all_are_contiguous_components_in_same_logical_voice(self)
        durations = [durationtools.Duration(x) for x in durations]
        if cyclic:
            durations = sequencetools.CyclicTuple(durations)
        result = []
        part = []
        current_duration_index = 0
        target_duration = durations[current_duration_index]
        cumulative_duration = durationtools.Duration(0)
        components_copy = list(self)
        while True:
            try:
                component = components_copy.pop(0)
            except IndexError:
                break
            component_duration = component._get_duration()
            if in_seconds:
                component_duration = component._get_duration(in_seconds=True)
            candidate_duration = cumulative_duration + component_duration
            if candidate_duration < target_duration:
                part.append(component)
                cumulative_duration = candidate_duration
            elif candidate_duration == target_duration:
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = durationtools.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
            elif target_duration < candidate_duration:
                if fill == 'exact':
                    raise PartitionError
                elif fill == 'less':
                    result.append(part)
                    part = [component]
                    if in_seconds:
                        cumulative_duration = \
                            sum([x._get_duration(in_seconds=True) 
                            for x in part])
                    else:
                        cumulative_duration = \
                            sum([x._get_duration() for x in part])
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
                    if target_duration < cumulative_duration:
                        message = 'target duration {}'
                        message += ' is less than cumulative duration {}.'
                        message = message.format(
                            target_duration, cumulative_duration)
                        raise PartitionError(message)
                elif fill == 'greater':
                    part.append(component)
                    result.append(part)
                    part = []
                    cumulative_duration = durationtools.Duration(0)
                    current_duration_index += 1
                    try:
                        target_duration = durations[current_duration_index]
                    except IndexError:
                        break
        if len(part):
            if overhang:
                result.append(part)
        if len(components_copy):
            if overhang:
                result.append(components_copy)
        return result

    def partition_by_durations_exactly(
        self,
        durations,
        cyclic=False,
        in_seconds=False,
        overhang=False,
        ):
        return self.partition_by_durations(
            durations,
            cyclic=cyclic,
            fill='exact',
            in_seconds=in_seconds,
            overhang=overhang,
            )

    def partition_by_durations_not_greater_than(
        self,
        durations,
        cyclic=False,
        in_seconds=False,
        overhang=False,
        ):
        return self.partition_by_durations(
            durations,
            cyclic=cyclic,
            fill='less',
            in_seconds=in_seconds,
            overhang=overhang,
            )

    def partition_by_durations_not_less_than(
        self,
        durations,
        cyclic=False,
        in_seconds=False,
        overhang=False,
        ):
        return self.partition_by_durations(
            durations,
            cyclic=cyclic,
            fill='greater',
            in_seconds=in_seconds,
            overhang=overhang,
            )
