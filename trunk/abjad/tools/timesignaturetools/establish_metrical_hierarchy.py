# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import mathtools
from abjad.tools import mutationtools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
Selection = selectiontools.Selection


def establish_metrical_hierarchy(
    components,
    metrical_hierarchy,
    boundary_depth=None,
    maximum_dot_count=None,
    ):
    r'''Rewrite the contents of tie chains in an expression to match a metrical
    hierarchy.

    ..  container:: example

        **Example 1.** Rewrite the contents of a measure in a staff using the 
        default metrical hierarchy for that measure's time signature:

        ::

            >>> parseable = "abj: | 2/4 c'2 ~ |"
            >>> parseable += "| 4/4 c'32 d'2.. ~ d'16 e'32 ~ |"
            >>> parseable += "| 2/4 e'2 |"
            >>> staff = Staff(parseable)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/4
                    c'2 ~
                }
                {
                    \time 4/4
                    c'32
                    d'2.. ~
                    d'16
                    e'32 ~
                }
                {
                    \time 2/4
                    e'2
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
            >>> print hierarchy.pretty_rtm_format
            (4/4 (
                1/4
                1/4
                1/4
                1/4))

        ::

            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     staff[1][:],
            ...     hierarchy,
            ...     )

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/4
                    c'2 ~
                }
                {
                    \time 4/4
                    c'32
                    d'8.. ~
                    d'2 ~
                    d'8..
                    e'32 ~
                }
                {
                    \time 2/4
                    e'2
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Rewrite the contents of a measure in a staff using a 
        custom metrical hierarchy:

        ::

            >>> staff = Staff(parseable)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/4
                    c'2 ~
                }
                {
                    \time 4/4
                    c'32
                    d'2.. ~
                    d'16
                    e'32 ~
                }
                {
                    \time 2/4
                    e'2
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> rtm = '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
            >>> hierarchy = timesignaturetools.MetricalHierarchy(rtm)
            >>> print hierarchy.pretty_rtm_format # doctest: +SKIP
            (4/4 (
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

        ::

            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     staff[1][:],
            ...     hierarchy,
            ...     )

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/4
                    c'2 ~
                }
                {
                    \time 4/4
                    c'32
                    d'4... ~
                    d'4...
                    e'32 ~
                }
                {
                    \time 2/4
                    e'2
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 3.** Limit the maximum number of dots per leaf using 
        `maximum_dot_count`:

        ::

            >>> parseable = "abj: | 3/4 c'32 d'8 e'8 fs'4... |"
            >>> measure = p(parseable)

        ..  doctest::

            >>> f(measure)
            {
                \time 3/4
                c'32
                d'8
                e'8
                fs'4...
            }

        ::

            >>> show(measure) # doctest: +SKIP

        Without constraining the `maximum_dot_count`:

        ::

            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 3/4
                c'32
                d'16. ~
                d'32
                e'16. ~
                e'32
                fs'4...
            }

        ::

            >>> show(measure) # doctest: +SKIP

        Constraining the `maximum_dot_count` to `2`:

        ::

            >>> measure = p(parseable)
            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     maximum_dot_count=2,
            ...     )

        ..  doctest::
        
            >>> f(measure)
            {
                \time 3/4
                c'32
                d'16. ~
                d'32
                e'16. ~
                e'32
                fs'8.. ~
                fs'4
            }

        ::

            >>> show(measure) # doctest: +SKIP

        Constraining the `maximum_dot_count` to `1`:

        ::

            >>> measure = p(parseable)
            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     maximum_dot_count=1,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 3/4
                c'32
                d'16. ~
                d'32
                e'16. ~
                e'32
                fs'16. ~
                fs'8 ~
                fs'4
            }

        ::

            >>> show(measure) # doctest: +SKIP

        Constraining the `maximum_dot_count` to `0`:

        ::

            >>> measure = p(parseable)
            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     maximum_dot_count=0,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 3/4
                c'32
                d'32 ~
                d'16 ~
                d'32
                e'32 ~
                e'16 ~
                e'32
                fs'32 ~
                fs'16 ~
                fs'8 ~
                fs'4
            }

        ::

            >>> show(measure) # doctest: +SKIP

    ..  container:: example

        **Example 4.** Split tie chains at different depths of the 
        `MetricalHierarchy`, if those tie chains cross any offsets at that 
        depth, but do not also both begin and end at any of those offsets.  

        Consider the default metrical hierarchy for `9/8`:

        ::

            >>> hierarchy = timesignaturetools.MetricalHierarchy((9, 8))
            >>> print hierarchy.pretty_rtm_format
            (9/8 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))

        We can establish that hierarchy without specifying a `boundary_depth`:

        ::

            >>> parseable = "abj: | 9/8 c'2 d'2 e'8 |"
            >>> measure = p(parseable)

        ..  doctest::
        
            >>> f(measure)
            {
                \time 9/8
                c'2
                d'2
                e'8
            }

        ::

            >>> show(measure) # doctest: +SKIP

        ::

            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 9/8
                c'2
                d'4 ~
                d'4
                e'8
            }

        ::

            >>> show(measure) # doctest: +SKIP

        With a `boundary_depth` of `1`, tie chains which cross any offsets 
        created by nodes with a depth of `1` in this MetricalHierarchy's rhythm 
        tree - i.e.  `0/8`, `3/8`, `6/8` and `9/8` - which do not also begin 
        and end at any of those offsets, will be split:

        ::

            >>> measure = p(parseable)
            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     boundary_depth=1,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 9/8
                c'4. ~
                c'8
                d'4 ~
                d'4
                e'8
            }

        ::

            >>> show(measure) # doctest: +SKIP

        For this `9/8` hierarchy, and this input notation, A `boundary_depth` 
        of `2` causes no change, as all tie chains already align to multiples 
        of `1/8`:

        ::

            >>> measure = p(parseable)
            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     boundary_depth=2,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 9/8
                c'2
                d'4 ~
                d'4
                e'8
            }

        ::

            >>> show(measure) # doctest: +SKIP

    ..  container:: example

        **Example 5.** Comparison of `3/4` and `6/8`, at `boundary_depths` of 0 
        and 1:

        ::

            >>> triple = "abj: | 3/4 2 4 || 3/4 4 2 || 3/4 4. 4. |"
            >>> triple += "| 3/4 2 ~ 8 8 || 3/4 8 8 ~ 2 |"
            >>> duples = "abj: | 6/8 2 4 || 6/8 4 2 || 6/8 4. 4. |"
            >>> duples += "| 6/8 2 ~ 8 8 || 6/8 8 8 ~ 2 |"
            >>> score = Score([Staff(triple), Staff(duples)])

        In order to see the different time signatures on each staff, we need to
        move some engravers from the Score context to the Staff context:

        ::

            >>> engravers = ['Timing_translator', 'Time_signature_engraver',
            ...     'Default_bar_line_engraver']
            >>> score.engraver_removals.extend(engravers)
            >>> score[0].engraver_consists.extend(engravers)
            >>> score[1].engraver_consists.extend(engravers)

        ..  doctest::

            >>> f(score)
            \new Score \with {
                \remove Timing_translator
                \remove Time_signature_engraver
                \remove Default_bar_line_engraver
            } <<
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 3/4
                        c'2
                        c'4
                    }
                    {
                        c'4
                        c'2
                    }
                    {
                        c'4.
                        c'4.
                    }
                    {
                        c'2 ~
                        c'8
                        c'8
                    }
                    {
                        c'8
                        c'8 ~
                        c'2
                    }
                }
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 6/8
                        c'2
                        c'4
                    }
                    {
                        c'4
                        c'2
                    }
                    {
                        c'4.
                        c'4.
                    }
                    {
                        c'2 ~
                        c'8
                        c'8
                    }
                    {
                        c'8
                        c'8 ~
                        c'2
                    }
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Here we establish a metrical hierarchy without specifying and boundary 
        depth:

        ::

            >>> for measure in iterationtools.iterate_measures_in_expr(score):
            ...     timesignaturetools.establish_metrical_hierarchy(
            ...         measure[:],
            ...         measure,
            ...         )

        ..  doctest::

            >>> f(score)
            \new Score \with {
                \remove Timing_translator
                \remove Time_signature_engraver
                \remove Default_bar_line_engraver
            } <<
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 3/4
                        c'2
                        c'4
                    }
                    {
                        c'4
                        c'2
                    }
                    {
                        c'4.
                        c'4.
                    }
                    {
                        c'2 ~
                        c'8
                        c'8
                    }
                    {
                        c'8
                        c'8 ~
                        c'2
                    }
                }
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 6/8
                        c'2
                        c'4
                    }
                    {
                        c'4
                        c'2
                    }
                    {
                        c'4.
                        c'4.
                    }
                    {
                        c'4. ~
                        c'4
                        c'8
                    }
                    {
                        c'8
                        c'4 ~
                        c'4.
                    }
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Here we re-establish metrical hierarchy at a boundary depth of `1`:

        ::

            >>> for measure in iterationtools.iterate_measures_in_expr(score):
            ...     timesignaturetools.establish_metrical_hierarchy(
            ...         measure[:],
            ...         measure,
            ...         boundary_depth=1,
            ...         )
            ...

        ..  doctest::

            >>> f(score)
            \new Score \with {
                \remove Timing_translator
                \remove Time_signature_engraver
                \remove Default_bar_line_engraver
            } <<
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 3/4
                        c'2
                        c'4
                    }
                    {
                        c'4
                        c'2
                    }
                    {
                        c'4 ~
                        c'8
                        c'8 ~
                        c'4
                    }
                    {
                        c'2 ~
                        c'8
                        c'8
                    }
                    {
                        c'8
                        c'8 ~
                        c'2
                    }
                }
                \new Staff \with {
                    \consists Timing_translator
                    \consists Time_signature_engraver
                    \consists Default_bar_line_engraver
                } {
                    {
                        \time 6/8
                        c'4. ~
                        c'8
                        c'4
                    }
                    {
                        c'4
                        c'8 ~
                        c'4.
                    }
                    {
                        c'4.
                        c'4.
                    }
                    {
                        c'4. ~
                        c'4
                        c'8
                    }
                    {
                        c'8
                        c'4 ~
                        c'4.
                    }
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Note that the two time signatures are much more clearly disambiguated above.

    ..  container:: example

        **Example 6.** Establishing metrical hierarchy recursively in measures 
        with nested tuplets:

        ::

            >>> parseable = "abj: | 4/4 c'16 ~ c'4 d'8. ~ "
            >>> parseable += "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } "
            >>> parseable += "f'4 |"
            >>> measure = p(parseable)

        ..  doctest::
        
            >>> f(measure)
            {
                \time 4/4
                c'16 ~
                c'4
                d'8. ~
                \times 2/3 {
                    d'8. ~
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        d'16
                        e'8.
                        f'16 ~
                    }
                }
                f'4
            }

        ::

            >>> show(measure) # doctest: +SKIP

        When establishing a metrical hierarchy on a selection of components 
        which contain containers, like `Tuplets` or `Containers`,
        `timesignaturetools.establish_metrical_hierarchy()` will recurse into
        those containers, treating them as measures whose time signature is 
        derived from the preprolated preprolated_duration of the container's 
        contents:

        ::

            >>> timesignaturetools.establish_metrical_hierarchy(
            ...     measure[:],
            ...     measure,
            ...     boundary_depth=1,
            ...     )

        ..  doctest::

            >>> f(measure)
            {
                \time 4/4
                c'4 ~
                c'16
                d'8. ~
                \times 2/3 {
                    d'8 ~
                    d'16 ~
                    \tweak #'text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        d'16
                        e'8 ~
                        e'16
                        f'16 ~
                    }
                }
                f'4
            }

        ::

            >>> show(measure) # doctest: +SKIP

    Operates in place and returns none.
    '''
    from abjad.tools import timesignaturetools

    def get_offsets_at_depth(depth):
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in \
                sequencetools.iterate_sequence_pairwise_strict(old_offsets):
                new_offsets.append(first)
                new_offsets.append((first + second) / 2)
            new_offsets.append(old_offsets[-1])
            offset_inventory.append(tuple(new_offsets))
        return offset_inventory[depth]

    def is_acceptable_tie_chain(tie_chain_duration,
        tie_chain_starts_in_offsets,
        tie_chain_stops_in_offsets):
        #print '\tTESTING ACCEPTABILITY'
        if not tie_chain_duration.is_assignable:
            return False
        if maximum_dot_count is not None and \
            maximum_dot_count < tie_chain_duration.dot_count:
            return False
        if not tie_chain_starts_in_offsets and not tie_chain_stops_in_offsets:
            return False
        return True

    def is_boundary_crossing_tie_chain(
        tie_chain_start_offset, tie_chain_stop_offset):
        #print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(tie_chain_start_offset < x < tie_chain_stop_offset 
            for x in boundary_offsets):
            return False
        if tie_chain_start_offset in boundary_offsets and \
            tie_chain_stop_offset in boundary_offsets:
            return False
        return True

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        #print 'DEPTH:', depth

        tie_chain_duration = tie_chain._preprolated_duration
        tie_chain_start_offset = tie_chain.get_timespan().start_offset
        tie_chain_stop_offset = tie_chain.get_timespan().stop_offset
        tie_chain_starts_in_offsets = tie_chain_start_offset in offsets
        tie_chain_stops_in_offsets = tie_chain_stop_offset in offsets

        if not is_acceptable_tie_chain(
            tie_chain_duration,
            tie_chain_starts_in_offsets,
            tie_chain_stops_in_offsets):

            #print 'UNACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            split_offset = None
            offsets = get_offsets_at_depth(depth)

            # If the tie chain's start aligns, take the latest possible offset.
            if tie_chain_starts_in_offsets:
                offsets = reversed(offsets)

            for offset in offsets:
                if tie_chain_start_offset < offset < tie_chain_stop_offset:
                    split_offset = offset
                    break

            #print '\tABS:', split_offset
            if split_offset is not None:
                split_offset -= tie_chain_start_offset
                #print '\tREL:', split_offset
                #print ''
                shards = \
                    mutationtools.mutate(tie_chain[:]).split([split_offset])
                tie_chains = \
                    [selectiontools.TieChain(shard) for shard in shards]
                for tie_chain in tie_chains:
                    recurse(tie_chain, depth=depth)
            else:
                #print ''
                recurse(tie_chain, depth=depth+1)

        elif is_boundary_crossing_tie_chain(
            tie_chain_start_offset,
            tie_chain_stop_offset):

            #print 'BOUNDARY CROSSING', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            offsets = boundary_offsets
            if tie_chain_start_offset in boundary_offsets:
                offsets = reversed(boundary_offsets)
            split_offset = None
            for offset in offsets:
                if tie_chain_start_offset < offset < tie_chain_stop_offset:
                    split_offset = offset
                    break
            assert split_offset is not None
            #print '\tABS:', split_offset
            split_offset -= tie_chain_start_offset
            #print '\tREL:', split_offset
            #print ''
            shards = \
                mutationtools.mutate(tie_chain[:]).split([split_offset])
            tie_chains = \
                [selectiontools.TieChain(shard) for shard in shards]
            for tie_chain in tie_chains:
                recurse(tie_chain, depth=depth)

        else:
            #print 'ACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            #print ''
            tie_chain[:]._fuse()

    # Validate arguments.
    assert Selection._all_are_contiguous_components_in_same_logical_voice(
        components)
    if not isinstance(metrical_hierarchy,
        timesignaturetools.MetricalHierarchy):
        metrical_hierarchy = \
            timesignaturetools.MetricalHierarchy(metrical_hierarchy)
    assert sum([x._preprolated_duration for x in components]) == \
        metrical_hierarchy.preprolated_duration
    if boundary_depth is not None:
        boundary_depth = int(boundary_depth)
    if maximum_dot_count is not None:
        maximum_dot_count = int(maximum_dot_count)
        assert 0 <= maximum_dot_count

    # Build offset inventory, adjusted for initial offset and prolation.
    first_offset = components[0]._get_timespan().start_offset
    prolation = components[0]._get_parentage(include_self=False).prolation
    offset_inventory= []
    for offsets in metrical_hierarchy.depthwise_offset_inventory:
        offsets = [(x * prolation) + first_offset for x in offsets]
        offset_inventory.append(tuple(offsets))

    # Build boundary offset inventory, if applicable.
    if boundary_depth is not None:
        boundary_offsets = offset_inventory[boundary_depth]

    # Cache results of iterator, as we'll be mutating the underlying collection.
    items = tuple(_iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(components))
    for item in items:
        if isinstance(item, selectiontools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            preprolated_duration = sum([x._preprolated_duration for x in item])
            if preprolated_duration.numerator == 1:
                preprolated_duration = mathtools.NonreducedFraction(
                    preprolated_duration)
                preprolated_duration = preprolated_duration.with_denominator(
                    preprolated_duration.denominator * 4)
            sub_metrical_hierarchy = timesignaturetools.MetricalHierarchy(preprolated_duration)
            sub_boundary_depth = 1
            if boundary_depth is None:
                sub_boundary_depth = None
            establish_metrical_hierarchy(
                item[:],
                sub_metrical_hierarchy,
                boundary_depth=sub_boundary_depth,
                maximum_dot_count=maximum_dot_count,
                )
   

def _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
    expr):
    r'''Iterate topmost masked tie chains, rest groups and containers in
    `expr`, masked by `expr`:

    ::

        >>> input = "abj: | 2/4 c'4 d'4 ~ |"
        >>> input += "| 4/4 d'8. r16 r8. e'16 ~ 2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ |"
        >>> input += "| 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ |"
        >>> input += "| 2/4 b'4 c''4 |"
        >>> staff = Staff(input)

    ..  doctest::

        >>> f(staff)
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

        >>> from abjad.tools.timesignaturetools.establish_metrical_hierarchy \
        ...     import _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[0]): x
        ...
        TieChain(Note("c'4"),)
        TieChain(Note("d'4"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[1]): x
        ...
        TieChain(Note("d'8."),)
        TieChain(Rest('r16'), Rest('r8.'))
        TieChain(Note("e'16"),)
        Tuplet(2/3, [e'8, e'8, f'8])
        TieChain(Note("f'4"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[2]): x
        ...
        TieChain(Note("f'8"),)
        TieChain(Note("g'8"), Note("g'4"))
        TieChain(Note("a'4"), Note("a'8"))
        TieChain(Note("b'8"),)

    ::

        >>> for x in _iterate_topmost_masked_tie_chains_rest_groups_and_containers_in_expr(
        ...     staff[3]): x
        ...
        TieChain(Note("b'4"),)
        TieChain(Note("c''4"),)

    Returns generator.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import resttools
    from abjad.tools import selectiontools
    from abjad.tools import skiptools
    from abjad.tools import spannertools

    last_tie_spanner = None
    current_leaf_group = None
    current_leaf_group_is_silent = False

    for x in expr:
        if isinstance(x, (notetools.Note, chordtools.Chord)):
            this_tie_spanner = x._get_spanners(spannertools.TieSpanner) or None
            if current_leaf_group is None:
                current_leaf_group = []
            elif current_leaf_group_is_silent or \
                this_tie_spanner is None or \
                last_tie_spanner != this_tie_spanner:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = False
            current_leaf_group.append(x)
            last_tie_spanner = this_tie_spanner
        elif isinstance(x, (resttools.Rest, skiptools.Skip)):
            if current_leaf_group is None:
                current_leaf_group = []
            elif not current_leaf_group_is_silent:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = True
            current_leaf_group.append(x)
            last_tie_spanner = None
        elif isinstance(x, containertools.Container):
            if current_leaf_group is not None:
                yield selectiontools.TieChain(current_leaf_group)
                current_leaf_group = None
                last_tie_spanner = None
            yield x

        else:
            raise Exception('unhandled component found {!r}', x)
    if current_leaf_group is not None:
        yield selectiontools.TieChain(current_leaf_group)
