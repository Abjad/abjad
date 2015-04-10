# -*- encoding: utf-8 -*-
import copy
import itertools
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate
from abjad.tools.selectiontools.Selection import Selection


class ContiguousSelection(Selection):
    r'''A time-contiguous selection of components.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        music = self._coerce_music(music)
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Adds `expr` to selection.

        Returns new selection.
        '''
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
        '''Adds selection to `expr`.

        Returns new selection.
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

    def _attach_tie_spanner_to_leaf_pair(self, use_messiaen_style_ties=False):
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, scoretools.Leaf), left_leaf
        assert isinstance(right_leaf, scoretools.Leaf), right_leaf
        left_logical_tie = left_leaf._get_logical_tie()
        right_logical_tie = right_leaf._get_logical_tie()
        prototype = (spannertools.Tie,)
        if left_logical_tie == right_logical_tie:
            return
        try:
            left_tie_spanner = left_leaf._get_spanner(prototype)
        except MissingSpannerError:
            left_tie_spanner = None
        try:
            right_tie_spanner = right_leaf._get_spanner(prototype)
        except MissingSpannerError:
            right_tie_spanner = None
        if left_tie_spanner is not None and right_tie_spanner is not None:
            left_tie_spanner._fuse_by_reference(right_tie_spanner)
        elif left_tie_spanner is not None and right_tie_spanner is None:
            left_tie_spanner._append(right_leaf)
        elif left_tie_spanner is None and right_tie_spanner is not None:
            right_tie_spanner._append_left(left_leaf)
        elif left_tie_spanner is None and right_tie_spanner is None:
            tie = spannertools.Tie(
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            attach(tie, [left_leaf, right_leaf])

    def _copy(self, n=1, include_enclosing_containers=False):
        r'''Copies components in selection and fractures crossing spanners.

        Components in selection must be logical-voice-contiguous.

        The steps this function takes are as follows:

            * Deep copy `components`.

            * Deep copy spanners that attach to any component in `components`.

            * Fracture spanners that attach to components not in `components`.

            * Returns Python list of copied components.

        ..  container:: example

            **Example 1.** Copy components one time:

            ::

                >>> staff = Staff(r"c'8 ( d'8 e'8 f'8 )")
                >>> staff.append(r"g'8 a'8 b'8 c''8")
                >>> time_signature = TimeSignature((2, 4))
                >>> attach(time_signature, staff)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
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

                >>> print(format(new_staff))
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

                >>> print(format(new_staff))
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

                >>> print(format(staff))
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

                >>> print(format(new_staff))
                \new Staff {
                    \new Voice {
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'4
                            e'4
                        }
                        \tweak #'edge-height #'(0.7 . 0)
                        \times 2/3 {
                            f'4
                            e'4
                        }
                    }
                }

        Returns contiguous selection.
        '''
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        # check input
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        # return empty list when nothing to copy
        if n < 1:
            return []
        new_components = [
            component._copy_with_children_and_indicators_but_without_spanners()
            for component in self
            ]
        if include_enclosing_containers:
            return self._copy_and_include_enclosing_containers()
        new_components = type(self)(new_components)
        # make schema of spanners contained by components
        schema = self._make_spanner_schema()
        # copy spanners covered by components
        for covered_spanner, component_indices in list(schema.items()):
            new_covered_spanner = copy.copy(covered_spanner)
            del(schema[covered_spanner])
            schema[new_covered_spanner] = component_indices
        # reverse schema
        reversed_schema = {}
        for new_covered_spanner, component_indices in list(schema.items()):
            for component_index in component_indices:
                try:
                    reversed_schema[component_index].append(
                        new_covered_spanner)
                except KeyError:
                    reversed_schema[component_index] = [new_covered_spanner]
        # iterate components and add new components to new spanners
        for component_index, new_component in enumerate(
            iterate(new_components).by_class()):
            try:
                new_covered_spanners = reversed_schema[component_index]
                for new_covered_spanner in new_covered_spanners:
                    new_covered_spanner._append(new_component)
            except KeyError:
                pass
        # repeat as specified by input
        for i in range(n - 1):
            new_components += self._copy()
        # return new components
        return new_components

    def _copy_and_include_enclosing_containers(self):
        from abjad.tools import scoretools
        # get governor
        parentage = self[0]._get_parentage(include_self=True)
        governor = parentage._get_governor()
        # find start and stop indices in governor
        governor_leaves = list(governor.select_leaves())
        for i, x in enumerate(governor_leaves):
            if x is self[0]:
                start_index_in_governor = i
        for i, x in enumerate(governor_leaves):
            if x is self[-1]:
                stop_index_in_governor = i
        # copy governor
        governor_copy = mutate(governor).copy()
        copied_leaves = governor_copy.select_leaves()
        # find start and stop leaves in copy of governor
        start_leaf = copied_leaves[start_index_in_governor]
        stop_leaf = copied_leaves[stop_index_in_governor]
        # trim governor copy forwards from first leaf
        found_start_leaf = False
        while not found_start_leaf:
            leaf = next(iterate(governor_copy).by_class(scoretools.Leaf))
            if leaf is start_leaf:
                found_start_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # trim governor copy backwards from last leaf
        found_stop_leaf = False
        while not found_stop_leaf:
            reverse_iterator = iterate(governor_copy).by_class(
                scoretools.Leaf, reverse=True)
            leaf = next(reverse_iterator)
            if leaf is stop_leaf:
                found_stop_leaf = True
            else:
                leaf._remove_and_shrink_durated_parent_containers()
        # return trimmed governor copy
        return governor_copy

    def _fuse(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        if all(isinstance(x, scoretools.Leaf) for x in self):
            return self._fuse_leaves()
        elif all(isinstance(x, scoretools.Tuplet) for x in self):
            return self._fuse_tuplets()
        elif all(isinstance(x, scoretools.Measure) for x in self):
            return self._fuse_measures()
        else:
            message = 'can not fuse.'
            raise Exception(message)

    def _fuse_leaves(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        assert all(isinstance(x, scoretools.Leaf) for x in self)
        leaves = self
        if len(leaves) <= 1:
            return leaves
        total_preprolated = leaves._preprolated_duration
        for leaf in leaves[1:]:
            parent = leaf._parent
            if parent:
                index = parent.index(leaf)
                del(parent[index])
        return leaves[0]._set_duration(total_preprolated)

    def _fuse_measures(self):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        # check input
        prototype=(scoretools.Measure,)
        assert self._all_are_contiguous_components_in_same_parent(
            self, prototype)
        # return none on empty measures
        if len(self) == 0:
            return None
        # TODO: instantiate a new measure
        #       instead of returning a reference to existing measure
        if len(self) == 1:
            return self[0]
        implicit_scaling = self[0].implicit_scaling
        assert all(
            x.implicit_scaling == implicit_scaling for x in self)
        selection = selectiontools.SliceSelection(self)
        parent, start, stop = selection._get_parent_and_start_stop_indices()
        old_denominators = []
        new_duration = durationtools.Duration(0)
        for measure in self:
            effective_time_signature = measure.time_signature
            old_denominators.append(effective_time_signature.denominator)
            new_duration += effective_time_signature.duration
        new_time_signature = \
            measure._duration_and_possible_denominators_to_time_signature(
            new_duration,
            old_denominators,
            )
        music = []
        for measure in self:
            # scale before reassignment to prevent logical tie scale drama
            signature = measure.time_signature
            prolation = signature.implied_prolation
            multiplier = prolation / new_time_signature.implied_prolation
            measure._scale_contents(multiplier)
            measure_music = measure[:]
            measure_music._set_parents(None)
            music += measure_music
        new_measure = scoretools.Measure(new_time_signature, music)
        new_measure.implicit_scaling = self[0].implicit_scaling
        if parent is not None:
            self._give_dominant_spanners([new_measure])
        self._set_parents(None)
        if parent is not None:
            parent.insert(start, new_measure)
        return new_measure

    def _fuse_tuplets(self):
        from abjad.tools import scoretools
        assert self._all_are_contiguous_components_in_same_parent(
            self, prototype=(scoretools.Tuplet,))
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                message = 'tuplets must carry same multiplier.'
                raise ValueError(message)
            if type(tuplet) != first_type:
                message = 'tuplets must be same type.'
                raise TypeError(message)
        if isinstance(first, scoretools.FixedDurationTuplet):
            total_contents_duration = sum(
                [x._contents_duration for x in self])
            new_target_duration = first_multiplier * total_contents_duration
            new_tuplet = scoretools.FixedDurationTuplet(
                new_target_duration, [])
        elif isinstance(first, scoretools.Tuplet):
            new_tuplet = scoretools.Tuplet(first_multiplier, [])
        else:
            message = 'unknown tuplet type.'
            raise TypeError(message)
        wrapped = False
        if self[0]._get_parentage().root is not \
            self[-1]._get_parentage().root:
            dummy_container = scoretools.Container(self)
            wrapped = True
        mutate(self).swap(new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet

    def _get_crossing_spanners(self):
        r'''Assert logical-voice-contiguous components.
        Collect spanners that attach to any component in selection.
        Returns unordered set of crossing spanners.
        A spanner P crosses a list of logical-voice-contiguous components C
        when P and C share at least one component and when it is the
        case that NOT ALL of the components in P are also in C.
        In other words, there is some intersection -- but not total
        intersection -- between the components of P and C.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        all_components = set(iterate(self).by_class())
        contained_spanners = set()
        for component in iterate(self).by_class():
            contained_spanners.update(component._get_spanners())
        crossing_spanners = set([])
        for spanner in contained_spanners:
            spanner_components = set(spanner[:])
            if not spanner_components.issubset(all_components):
                crossing_spanners.add(spanner)
        return crossing_spanners

    def _get_dominant_spanners(self):
        r'''Returns spanners that dominate components in selection.
        Returns set of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in selection together with the start index
        at which spanner first encounters selection.
        Use this helper to lift spanners temporarily from components
        in selection and perform some action to the underlying
        score tree before reattaching spanners.
        score components.
        '''
        from abjad.tools import selectiontools
        from abjad.tools import spannertools
        Selection = selectiontools.Selection
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        receipt = set([])
        if len(self) == 0:
            return receipt
        first, last = self[0], self[-1]
        start_components = first._get_descendants_starting_with()
        stop_components = last._get_descendants_stopping_with()
        stop_components = set(stop_components)
        for component in start_components:
            for spanner in component._get_spanners():
                if set(spanner[:]) & stop_components != set([]):
                    index = spanner._index(component)
                    receipt.add((spanner, index))
        return receipt

    def _get_offset_lists(self):
        start_offsets, stop_offsets = [], []
        for component in self:
            start_offsets.append(component._get_timespan().start_offset)
            stop_offsets.append(component._get_timespan().stop_offset)
        return start_offsets, stop_offsets

    def _give_dominant_spanners(self, recipients):
        r'''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Returns none.
        Not composer-safe.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        assert self._all_are_contiguous_components_in_same_logical_voice(
            recipients)
        receipt = self._get_dominant_spanners()
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    def _make_spanner_schema(self):
        schema = {}
        spanners = set()
        for component in iterate(self).by_class():
            spanners.update(component._get_spanners())
        for spanner in spanners:
            schema[spanner] = []
        for i, component in \
            enumerate(iterate(self).by_class()):
            attached_spanners = component._get_spanners()
            for attached_spanner in attached_spanners:
                try:
                    schema[attached_spanner].append(i)
                except KeyError:
                    pass
        return schema

    def _withdraw_from_crossing_spanners(self):
        r'''Not composer-safe.
        '''
        assert self._all_are_contiguous_components_in_same_logical_voice(self)
        crossing_spanners = self._get_crossing_spanners()
        components_including_children = list(iterate(self).by_class())
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner._components[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._components.remove(component)
                    component._spanners.discard(crossing_spanner)

    ### PUBLIC METHODS ###

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of contiguous selection.

        Returns timespan.
        '''
        from abjad.tools import timespantools
        if in_seconds:
            raise NotImplementedError
        timespan = self[0]._get_timespan()
        start_offset = timespan.start_offset
        stop_offset = timespan.stop_offset
        for x in self[1:]:
            timespan = x._get_timespan()
            if timespan.start_offset < start_offset:
                start_offset = timespan.start_offset
            if stop_offset < timespan.stop_offset:
                stop_offset = timespan.stop_offset
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
            durations = datastructuretools.CyclicTuple(durations)
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
        r'''Partitions components in selection by `durations` exactly.


        Returns list of selections.
        '''
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
        r'''Partitions components in selection by values of durations not
        greater than those in `durations`.

        Returns list of selections.
        '''
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
        r'''Partitions components in selection by values of durations not less
        than those in `durations`.

        Returns list of selections.
        '''
        return self.partition_by_durations(
            durations,
            cyclic=cyclic,
            fill='greater',
            in_seconds=in_seconds,
            overhang=overhang,
            )