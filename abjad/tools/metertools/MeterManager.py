# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import durationtools
from abjad.tools import sequencetools


class MeterManager(abctools.AbjadObject):
    r'''A meter manager.
    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def get_offsets_at_depth(depth, offset_inventory):
        r'''Gets offsets at `depth` in `offset_inventory`.
        '''
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in \
                sequencetools.iterate_sequence_nwise(old_offsets):
                new_offsets.append(first)
                difference = second - first
                half = (first + second) / 2
                if durationtools.Duration(1, 8) < difference:
                    new_offsets.append(half)
                else:
                    one_quarter = (first + half) / 2
                    three_quarters = (half + second) / 2
                    new_offsets.append(one_quarter)
                    new_offsets.append(half)
                    new_offsets.append(three_quarters)
            new_offsets.append(old_offsets[-1])
            offset_inventory.append(tuple(new_offsets))
        return offset_inventory[depth]

    @staticmethod
    def is_acceptable_logical_tie(
        logical_tie_duration=None,
        logical_tie_starts_in_offsets=None,
        logical_tie_stops_in_offsets=None,
        maximum_dot_count=None,
        ):
        r'''Is true if logical tie is acceptable.
        '''
        #print '\tTESTING ACCEPTABILITY'
        if not logical_tie_duration.is_assignable:
            return False
        if maximum_dot_count is not None and \
            maximum_dot_count < logical_tie_duration.dot_count:
            return False
        if not logical_tie_starts_in_offsets and \
            not logical_tie_stops_in_offsets:
            return False
        return True

    @staticmethod
    def is_boundary_crossing_logical_tie(
        boundary_depth=None,
        boundary_offsets=None,
        logical_tie_start_offset=None,
        logical_tie_stop_offset=None,
        ):
        r'''Is true if logical tie crosses meter boundaries.
        '''
        #print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(logical_tie_start_offset < x < logical_tie_stop_offset
            for x in boundary_offsets):
            return False
        if (logical_tie_start_offset in boundary_offsets and
            logical_tie_stop_offset in boundary_offsets):
            return False
        return True

    @staticmethod
    def iterate_rewrite_inputs(expr):
        r'''Iterates topmost masked logical ties, rest groups and containers
        in `expr`, masked by `expr`.

        ::

            >>> from abjad.tools import metertools
            >>> from abjad.tools import scoretools

        ::

            >>> string = "abj: ! 2/4 c'4 d'4 ~ !"
            >>> string += "! 4/4 d'8. r16 r8. e'16 ~ "
            >>> string += "2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ !"
            >>> string += "! 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ !"
            >>> string += "! 2/4 b'4 c''4 !"
            >>> string = string.replace('!', '|')
            >>> staff = scoretools.Staff(string)

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                {
                    \time 2/4
                    c'4
                    d'4 ~
                }
                {
                    \time 4/4
                    d'8.
                    r16
                    r8.
                    e'16 ~
                    \times 2/3 {
                        e'8 ~
                        e'8
                        f'8 ~
                    }
                    f'4 ~
                }
                {
                    f'8
                    g'8 ~
                    g'4
                    a'4 ~
                    a'8
                    b'8 ~
                }
                {
                    \time 2/4
                    b'4
                    c''4
                }
            }

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[0]): x
            ...
            LogicalTie([Note("c'4")])
            LogicalTie([Note("d'4")])

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[1]): x
            ...
            LogicalTie([Note("d'8.")])
            LogicalTie([Rest('r16'), Rest('r8.')])
            LogicalTie([Note("e'16")])
            Tuplet(Multiplier(2, 3), "e'8 ~ e'8 f'8 ~")
            LogicalTie([Note("f'4")])

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[2]): x
            ...
            LogicalTie([Note("f'8")])
            LogicalTie([Note("g'8"), Note("g'4")])
            LogicalTie([Note("a'4"), Note("a'8")])
            LogicalTie([Note("b'8")])

        ::

            >>> for x in metertools.MeterManager.iterate_rewrite_inputs(
            ...     staff[3]): x
            ...
            LogicalTie([Note("b'4")])
            LogicalTie([Note("c''4")])

        Returns generator.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        from abjad.tools import spannertools

        last_tie_spanner = None
        current_leaf_group = None
        current_leaf_group_is_silent = False

        for x in expr:
            if isinstance(x, (scoretools.Note, scoretools.Chord)):
                this_tie_spanner = x._get_spanners(spannertools.Tie) or None
                if current_leaf_group is None:
                    current_leaf_group = []
                elif current_leaf_group_is_silent or \
                    this_tie_spanner is None or \
                    last_tie_spanner != this_tie_spanner:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = False
                current_leaf_group.append(x)
                last_tie_spanner = this_tie_spanner
            elif isinstance(x, (scoretools.Rest, scoretools.Skip)):
                if current_leaf_group is None:
                    current_leaf_group = []
                elif not current_leaf_group_is_silent:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = True
                current_leaf_group.append(x)
                last_tie_spanner = None
            elif isinstance(x, scoretools.Container):
                if current_leaf_group is not None:
                    yield selectiontools.LogicalTie(current_leaf_group)
                    current_leaf_group = None
                    last_tie_spanner = None
                yield x

            else:
                message = 'unhandled component: {!r}.'
                message = message.format(x)
                raise Exception(message)
        if current_leaf_group is not None:
            yield selectiontools.LogicalTie(current_leaf_group)
