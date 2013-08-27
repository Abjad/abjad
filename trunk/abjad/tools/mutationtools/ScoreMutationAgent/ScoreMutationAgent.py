# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools


class ScoreMutationAgent(object):
    r'''A wrapper around the Abjad score mutators.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> leaves = staff[-2:]
            >>> show(staff) # doctest: +SKIP

        ::

            >>> mutate(leaves)
            ScoreMutationAgent(SliceSelection(Note("d'4"), Note("f'4")))

    '''

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Interpreter representation of score mutation agent.

        Returns string.
        '''
        return '{}({})'.format(
            self.__class__.__name__, self._client)

    ### PUBLIC METHODS ###

    def copy(self, n=1, include_enclosing_containers=False):
        r'''Copies component and fractures crossing spanners.

        Returns new component.
        '''
        from abjad.tools import componenttools
        from abjad.tools import selectiontools
        if isinstance(self._client, componenttools.Component):
            selection = selectiontools.ContiguousSelection(self._client)
        else:
            selection = self._client
        result = selection._copy(
            n=n,
            include_enclosing_containers=include_enclosing_containers,
            )
        if isinstance(self._client, componenttools.Component):
            if len(result) == 1:
                result = result[0]
        return result

    def divide(self, pitch=None):
        r'''Divides leaf at `pitch`.

        ..  container:: example

            **Example.** Divide chord at ``Eb4``:

                >>> chord = Chord("<d' ef' e'>4")
                >>> show(chord) # doctest: +SKIP

            ::

                >>> pitch = pitchtools.NamedPitch('Eb4')
                >>> upper, lower = mutate(chord).divide(pitch=pitch)
                >>> staff = Staff([upper, lower])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    <ef' e'>4
                    d'4
                }

        Set `pitch` to pitch, pitch name, pitch number or none.

        Sets `pitch` equal to ``B3`` when `pitch` is none.

        Defined against leaves only; not defined against containers.

        Returns pair of newly created leaves.
        '''
        return self._client._divide(
            pitch=pitch,
            )

    def replace(self, recipients):
        '''Move parentage and spanners from components to `recipients`.

        Almost exactly the same as container setitem logic.

        This function works with orphan components.

        Container setitem logic can not work with orphan components.

        Return none.
        '''
        from abjad.tools import componenttools
        from abjad.tools import selectiontools
        Selection = selectiontools.Selection
        # coerce input
        if isinstance(self._client, selectiontools.SliceSelection):
            donors = self._client
        else:
            donors = selectiontools.SliceSelection(self._client)
        if not isinstance(recipients, selectiontools.Selection):
            recipients = selectiontools.SliceSelection(recipients)
        # check input
        assert Selection._all_are_contiguous_components_in_same_parent(
            donors)
        assert Selection._all_are_contiguous_components_in_same_parent(
            recipients)
        # return donors unaltered when donors are empty
        if len(donors) == 0:
            #return donors
            return
        # give parentage and spanners to recipients
        parent, start, stop = donors._get_parent_and_start_stop_indices()
        if parent:
            parent.__setitem__(slice(start, stop + 1), recipients)
        else:
            donors._give_dominant_spanners_to_components(recipients)
            donors._withdraw_from_crossing_spanners()

    def shorten(self, duration):
        r'''Shortens component by `duration`.

        Returns none.
        '''
        return self._client._shorten(duration)

    def splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        r'''Splices `components` to the right or left of selection.

        Returns list of components.
        '''
        return self._client._splice(
            components,
            direction=direction, 
            grow_spanners=grow_spanners,
            )

    # TODO: fix bug that unintentionally fractures ties.
    # TODO: add tests of tupletted notes and rests.
    # TODO: add examples that show mark and context mark handling.
    # TODO: add example showing grace and after grace handling.
    def split(
        self, 
        durations,
        fracture_spanners=False, 
        cyclic=False, 
        tie_split_notes=True, 
        ):
        r'''Splits component or selection by `durations`.
        
        ..  container:: example

            **Example 1.** Split leaves:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff.select_leaves()
                >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
                >>> staff.override.dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations, 
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 
                    e'16
                    d'8
                    f'32 
                    f'16.
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

        ..  container:: example

            **Example 2.** Split leaves and fracture crossing spanners:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff.select_leaves()
                >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
                >>> staff.override.dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations, 
                ...     fracture_spanners=True, 
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 \f 
                    e'16 \< \p
                    d'8
                    f'32 \f 
                    f'16. \< \p
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

        ..  container:: example

            **Example 3.** Split leaves cyclically:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff.select_leaves()
                >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
                >>> staff.override.dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     cyclic=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 
                    e'16
                    d'8
                    f'32 
                    f'16.
                    c'16. 
                    c'32
                    e'8
                    d'16 
                    d'16
                    f'8 \f
                }

        ..  container:: example

            **Example 4.** Split leaves cyclically and fracture spanners:

            ::

                >>> staff = Staff("c'8 e' d' f' c' e' d' f'")
                >>> leaves = staff.select_leaves()
                >>> spanner = spannertools.HairpinSpanner(leaves, 'p < f')
                >>> staff.override.dynamic_line_spanner.staff_padding = 3
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'8
                    d'8
                    f'8
                    c'8
                    e'8
                    d'8
                    f'8 \f
                }

            ::

                >>> durations = [Duration(3, 16), Duration(7, 32)]
                >>> result = mutate(leaves).split(
                ...     durations,
                ...     cyclic=True, 
                ...     fracture_spanners=True,
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff \with {
                    \override DynamicLineSpanner #'staff-padding = #3
                } {
                    c'8 \< \p
                    e'16 \f 
                    e'16 \< \p
                    d'8
                    f'32 \f 
                    f'16. \< \p
                    c'16. \f 
                    c'32 \< \p
                    e'8
                    d'16 \f 
                    d'16 \< \p
                    f'8 \f
                }

        ..  container:: example

            **Example 5.** Split tupletted leaves and fracture 
                crossing spanners:

            ::

                >>> staff = Staff()
                >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
                >>> staff.append(Tuplet((2, 3), "c'4 d' e'"))
                >>> leaves = staff.select_leaves()
                >>> spanner = spannertools.SlurSpanner(leaves)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'4 (
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4 )
                    }
                }

            ::

                >>> durations = [Duration(1, 4)]
                >>> result = mutate(leaves).split(
                ...     durations, 
                ...     fracture_spanners=True, 
                ...     tie_split_notes=False,
                ...     )
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'4 (
                        d'8 ) 
                        d'8 (
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4 )
                    }
                }

        Returns list of selections.
        '''
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        from abjad.tools import selectiontools
        # check input
        components = self._client
        single_component_input = False
        if isinstance(components, componenttools.Component):
            single_component_input = True
            components = selectiontools.Selection(components)
        assert all(
            isinstance(x, componenttools.Component) for x in components)
        if not isinstance(components, selectiontools.Selection):
            components = selectiontools.Selection(components)
        durations = [durationtools.Duration(x) for x in durations]
        # return if no split to be done
        if not durations:
            if single_component_input:
                return components
            else:
                return [], components
        # calculate total component duration
        total_component_duration = components.get_duration()
        total_split_duration = sum(durations)
        # calculate durations
        if cyclic:
            durations = sequencetools.repeat_sequence_to_weight_exactly(
                durations, total_component_duration)
        elif total_split_duration < total_component_duration:
            final_offset = total_component_duration - sum(durations)
            durations.append(final_offset)
        elif total_component_duration < total_split_duration:
            durations = sequencetools.truncate_sequence_to_weight(
                durations, total_component_duration)
        # keep copy of durations to partition result components
        durations_copy = durations[:]
        # calculate total split duration
        total_split_duration = sum(durations)
        assert total_split_duration == total_component_duration
        # initialize loop variables
        result, shard = [], []
        offset_index, offset_count = 0, len(durations)
        current_shard_duration = durationtools.Duration(0)
        remaining_components = list(components[:])
        advance_to_next_offset = True
        # loop and build shards by grabbing next component 
        # and next duration each time through loop
        while True:
            # grab next split point
            if advance_to_next_offset:
                if durations:
                    next_split_point = durations.pop(0)
                else:
                    break
            advance_to_next_offset = True
            # grab next component from input stack of components
            if remaining_components:
                current_component = remaining_components.pop(0)
            else:
                break
            # find where current component endpoint will position us
            candidate_shard_duration = current_shard_duration + \
                current_component._get_duration()
            # if current component would fill current shard exactly
            if candidate_shard_duration == next_split_point:
                shard.append(current_component)
                result.append(shard)
                shard = []
                current_shard_duration = durationtools.Duration(0)
                offset_index += 1
            # if current component would exceed current shard
            elif next_split_point < candidate_shard_duration:
                local_split_duration = \
                    next_split_point - current_shard_duration
                if isinstance(current_component, leaftools.Leaf):
                    leaf_split_durations = [local_split_duration]
                    current_duration = current_component._get_duration()
                    additional_required_duration = \
                        current_duration - local_split_duration
                    split_durations = sequencetools.split_sequence_by_weights(
                        durations, 
                        [additional_required_duration], 
                        cyclic=False, 
                        overhang=True,
                        )
                    additional_durations = split_durations[0]
                    leaf_split_durations.extend(additional_durations)
                    durations = split_durations[-1]
                    leaf_shards = current_component._split(
                        leaf_split_durations,
                        cyclic=False, 
                        fracture_spanners=fracture_spanners,
                        tie_split_notes=tie_split_notes,
                        )
                    shard.extend(leaf_shards)
                    result.append(shard)
                    offset_index += len(additional_durations)
                else:
                    left_list, right_list = \
                        current_component._split_by_duration(
                        local_split_duration, 
                        fracture_spanners=fracture_spanners,
                        tie_split_notes=tie_split_notes, 
                        )
                    shard.extend(left_list)
                    result.append(shard)
                    remaining_components.__setitem__(slice(0, 0), right_list)
                shard = []
                offset_index += 1
                current_shard_duration = durationtools.Duration(0)
            # if current component would not fill current shard
            elif candidate_shard_duration < next_split_point:
                shard.append(current_component)
                current_shard_duration += current_component._get_duration()
                advance_to_next_offset = False
            else:
                raise ValueError
        # append any stub shard
        if len(shard):
            result.append(shard)
        # append any unexamined components
        if len(remaining_components):
            result.append(remaining_components)
        # partition split components according to input durations
        result = sequencetools.flatten_sequence(result)
        result = selectiontools.ContiguousSelection(result)
        result = result.partition_by_durations_exactly(durations_copy)
        # return list of shards
        result = [selectiontools.Selection(x) for x in result]
        return result
