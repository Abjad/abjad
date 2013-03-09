from abjad.tools import componenttools
from abjad.tools import leaftools
from abjad.tools import sequencetools
from abjad.tools import tietools


def establish_metrical_hierarchy(components, metrical_hierarchy,
    boundary_depth=None, maximum_dot_count=None):
    r'''.. versionadded:: 2.11

    Rewrite the contents of tie chains in an expression to match a metrical
    hierarchy.

    Example 1. Rewrite the contents of a measure in a staff using the default metrical
    hierarchy for that measure's time signature:

    ::

        >>> parseable = "abj: | 2/4 c'2 ~ || 4/4 c'32 d'2.. ~ d'16 e'32 ~ || 2/4 e'2 |"

    ::

        >>> staff = Staff(parseable)
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

        >>> timesignaturetools.establish_metrical_hierarchy(staff[1][:], hierarchy)
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

    Example 2. Rewrite the contents of a measure in a staff using a custom
    metrical hierarchy:

    ::

        >>> staff = Staff(parseable)
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

        >>> timesignaturetools.establish_metrical_hierarchy(staff[1][:], hierarchy)
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

    Example 3. Limit the maximum number of dots per leaf using
    `maximum_dot_count`:

    ::

        >>> parseable = "abj: | 3/4 c'32 d'8 e'8 fs'4... |"
        >>> measure = p(parseable)
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

        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure)
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
        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     maximum_dot_count=2)
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
        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     maximum_dot_count=1)
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
        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     maximum_dot_count=0)
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

    Example 4: Split tie chains at different depths of the `MetricalHierarchy`,
    if those tie chains cross any offsets at that depth, but do not also both
    begin and end at any of those offsets.

    Consider the default metrical hierarchy for `9/8`:

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

        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure)
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

    With a `boundary_depth` of `1`, tie chains which cross any offsets created
    by nodes with a depth of `1` in this MetricalHierarchy's rhythm tree - i.e.
    `0/8`, `3/8`, `6/8` and `9/8` - which do not also begin and end at any of those
    offsets, will be split:

    ::

        >>> measure = p(parseable)
        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     boundary_depth=1)
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

    For this `9/8` hierarchy, and this input notation, A `boundary_depth` of `2`
    causes no change, as all tie chains already align to multiples of `1/8`:

    ::

        >>> measure = p(parseable)
        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     boundary_depth=2)
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

    Example 5. Comparison of `3/4` and `6/8`, at `boundary_depths` of 0 and 1:

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

    Here we establish a metrical hierarchy without specifying and boundary depth:

    ::

        >>> for measure in iterationtools.iterate_measures_in_expr(score):
        ...     timesignaturetools.establish_metrical_hierarchy(measure[:], measure)
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
        ...         measure[:], measure, boundary_depth=1)
        ...
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

    Example 6. Establishing metrical hierarchy recursively in measures with
    nested tuplets:

    ::

        >>> measure = p("abj: | 4/4 c'16 ~ c'4 d'8. ~ " \
        ...     "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } f'4 |")
        >>> f(measure)
        {
            \time 4/4
            c'16 ~
            c'4
            d'8. ~
            \times 2/3 {
                d'8. ~
                \fraction \times 3/5 {
                    d'16
                    e'8.
                    f'16 ~
                }
            }
            f'4
        }

    ::

        >>> show(measure) # doctest: +SKIP

    When establishing a metrical hierarchy on a selection of components which
    contain containers, like `Tuplets` or `Containers`,
    `timesignaturetools.establish_metrical_hierarchy()` will recurse into
    those containers, treating them as measures whose time signature is derived
    from the preprolated preprolated_duration of the container's contents:

    ::

        >>> timesignaturetools.establish_metrical_hierarchy(measure[:], measure,
        ...     boundary_depth=1)
        >>> f(measure)
        {
            \time 4/4
            c'4 ~
            c'16
            d'8. ~
            \times 2/3 {
                d'8 ~
                d'16 ~
                \fraction \times 3/5 {
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

    Operate in place and return none.
    '''

    from abjad.tools import timesignaturetools

    def get_offsets_at_depth(depth):
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in sequencetools.iterate_sequence_pairwise_strict(old_offsets):
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

    def is_boundary_crossing_tie_chain(tie_chain_start_offset, tie_chain_stop_offset):
        #print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(tie_chain_start_offset < x < tie_chain_stop_offset for x in boundary_offsets):
            return False
        if tie_chain_start_offset in boundary_offsets and \
            tie_chain_stop_offset in boundary_offsets:
            return False
        return True

    def recurse(tie_chain, depth=0):
        offsets = get_offsets_at_depth(depth)
        #print 'DEPTH:', depth

        tie_chain_duration = tie_chain.preprolated_duration
        tie_chain_start_offset = tie_chain.start_offset
        tie_chain_stop_offset = tie_chain.stop_offset
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

            # if the tie chain's start aligns, take the latest possible offset
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
                tie_chains = [tietools.TieChain(shard) for shard in
                    componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
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
            tie_chains = [tietools.TieChain(shard) for shard in
                componenttools.split_components_at_offsets(tie_chain[:], [split_offset])]
            for tie_chain in tie_chains:
                recurse(tie_chain, depth=depth)

        else:
            #print 'ACCEPTABLE:', tie_chain, tie_chain_start_offset, tie_chain_stop_offset
            #print '\t', ' '.join([str(x) for x in offsets])
            #print ''
            leaftools.fuse_leaves(tie_chain[:])

    # check arguments
    assert componenttools.all_are_thread_contiguous_components(components)
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(metrical_hierarchy)
    assert sum([x.preprolated_duration for x in components]) == metrical_hierarchy.preprolated_duration
    if boundary_depth is not None:
        boundary_depth = int(boundary_depth)
    if maximum_dot_count is not None:
        maximum_dot_count = int(maximum_dot_count)
        assert 0 <= maximum_dot_count

    # build offset inventory, adjusted for initial offset and prolation
    first_offset = components[0].start_offset
    prolation = components[0].prolation
    offset_inventory= []
    for offsets in metrical_hierarchy.depthwise_offset_inventory:
        offsets = [(x * prolation) + first_offset for x in offsets]
        offset_inventory.append(tuple(offsets))

    # build boundary offset inventory, if applicable
    if boundary_depth is not None:
        boundary_offsets = offset_inventory[boundary_depth]

    # cache results of iterator, as we'll be mutating the underlying collection
    items = tuple(tietools.iterate_topmost_masked_tie_chains_and_containers_in_expr(components))
    for item in items:
        if isinstance(item, tietools.TieChain):
            #print 'RECURSING:', item
            recurse(item, depth=0)
        else:
            #print 'DESCENDING:', item
            preprolated_duration = sum([x.preprolated_duration for x in item])
            sub_metrical_hierarchy = timesignaturetools.MetricalHierarchy(preprolated_duration)
            sub_boundary_depth = 1
            if boundary_depth is None:
                sub_boundary_depth = None
            establish_metrical_hierarchy(item[:], sub_metrical_hierarchy,
                boundary_depth=sub_boundary_depth, maximum_dot_count=maximum_dot_count)
