# -*- coding: utf-8 -*-
from __future__ import print_function
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import mutate
Selection = selectiontools.Selection


def _rewrite_meter(
    components,
    meter,
    boundary_depth=None,
    initial_offset=None,
    maximum_dot_count=None,
    rewrite_tuplets=True,
    use_messiaen_style_ties=False,
    ):
    from abjad.tools import metertools
    from abjad.tools import scoretools

    assert isinstance(components, selectiontools.Selection), \
        repr(components)

    if not isinstance(meter, metertools.Meter):
        meter = metertools.Meter(meter)

    boundary_depth = boundary_depth or meter.preferred_boundary_depth

    def recurse(
        boundary_depth=None,
        boundary_offsets=None,
        depth=0,
        logical_tie=None,
        ):
        offsets = metertools.MeterManager.get_offsets_at_depth(
            depth,
            offset_inventory,
            )

        #print('DEPTH:', depth)

        logical_tie_duration = logical_tie._preprolated_duration
        logical_tie_timespan = logical_tie.get_timespan()
        logical_tie_start_offset = logical_tie_timespan.start_offset
        logical_tie_stop_offset = logical_tie_timespan.stop_offset
        logical_tie_starts_in_offsets = logical_tie_start_offset in offsets
        logical_tie_stops_in_offsets = logical_tie_stop_offset in offsets

        if not metertools.MeterManager.is_acceptable_logical_tie(
            logical_tie_duration=logical_tie_duration,
            logical_tie_starts_in_offsets=logical_tie_starts_in_offsets,
            logical_tie_stops_in_offsets=logical_tie_stops_in_offsets,
            maximum_dot_count=maximum_dot_count,
            ):

            #print('UNACCEPTABLE:', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
            #print('\t', ' '.join([str(x) for x in offsets]))
            split_offset = None
            offsets = metertools.MeterManager.get_offsets_at_depth(
                depth,
                offset_inventory,
                )

            # If the logical tie's start aligns, take the latest possible offset.
            if logical_tie_starts_in_offsets:
                offsets = reversed(offsets)

            for offset in offsets:
                if logical_tie_start_offset < offset < logical_tie_stop_offset:
                    split_offset = offset
                    break

            #print('\tABS:', split_offset)
            if split_offset is not None:
                split_offset -= logical_tie_start_offset
                #print('\tREL:', split_offset)
                #print()
                shards = mutate(logical_tie[:]).split(
                    [split_offset],
                    use_messiaen_style_ties=use_messiaen_style_ties,
                    )
                logical_ties = \
                    [selectiontools.LogicalTie(shard) for shard in shards]
                for logical_tie in logical_ties:
                    recurse(
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth,
                        logical_tie=logical_tie,
                        )
            else:
                #print()
                recurse(
                    boundary_depth=boundary_depth,
                    boundary_offsets=boundary_offsets,
                    depth=depth + 1,
                    logical_tie=logical_tie,
                    )

        elif metertools.MeterManager.is_boundary_crossing_logical_tie(
            boundary_depth=boundary_depth,
            boundary_offsets=boundary_offsets,
            logical_tie_start_offset=logical_tie_start_offset,
            logical_tie_stop_offset=logical_tie_stop_offset,
            ):

            #print('BOUNDARY CROSSING', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
            offsets = boundary_offsets
            if logical_tie_start_offset in boundary_offsets:
                offsets = reversed(boundary_offsets)
            split_offset = None
            for offset in offsets:
                if logical_tie_start_offset < offset < logical_tie_stop_offset:
                    split_offset = offset
                    break
            assert split_offset is not None
            #print('\tABS:', split_offset)
            split_offset -= logical_tie_start_offset
            #print('\tREL:', split_offset)
            #print()
            shards = mutate(logical_tie[:]).split(
                [split_offset],
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
            logical_ties = \
                [selectiontools.LogicalTie(shard) for shard in shards]
            for logical_tie in logical_ties:
                recurse(
                    boundary_depth=boundary_depth,
                    boundary_offsets=boundary_offsets,
                    depth=depth,
                    logical_tie=logical_tie,
                    )

        else:
            #print('ACCEPTABLE:', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
            #print('\t', ' '.join([str(x) for x in offsets]))
            #print()
            logical_tie[:]._fuse()

    # Validate arguments.
    assert Selection._all_are_contiguous_components_in_same_logical_voice(
        components)
    if not isinstance(meter,
        metertools.Meter):
        meter = \
            metertools.Meter(meter)

    #assert sum([x._preprolated_duration for x in components]) == \
    #    meter.preprolated_duration
    if boundary_depth is not None:
        boundary_depth = int(boundary_depth)
    if maximum_dot_count is not None:
        maximum_dot_count = int(maximum_dot_count)
        assert 0 <= maximum_dot_count

    if initial_offset is None:
        initial_offset = durationtools.Offset(0)
    initial_offset = durationtools.Offset(initial_offset)

    first_start_offset = inspect_(components[0]).get_timespan().start_offset
    last_start_offset = inspect_(components[-1]).get_timespan().start_offset
    difference = last_start_offset - first_start_offset + initial_offset
    assert difference < meter.implied_time_signature.duration

    # Build offset inventory, adjusted for initial offset and prolation.
    first_offset = components[0]._get_timespan().start_offset
    first_offset -= initial_offset
    prolation = components[0]._get_parentage(include_self=False).prolation
    offset_inventory = []
    for offsets in meter.depthwise_offset_inventory:
        offsets = [(x * prolation) + first_offset for x in offsets]
        offset_inventory.append(tuple(offsets))

    # Build boundary offset inventory, if applicable.
    if boundary_depth is not None:
        boundary_offsets = offset_inventory[boundary_depth]
    else:
        boundary_offsets = None

    # Cache results of iterator, as we'll be mutating the underlying collection
    iterator = metertools.MeterManager.iterate_rewrite_inputs(components)
    items = tuple(iterator)
    for item in items:
        if isinstance(item, selectiontools.LogicalTie):
            #print('RECURSING:', item)
            recurse(
                boundary_depth=boundary_depth,
                boundary_offsets=boundary_offsets,
                depth=0,
                logical_tie=item,
                )
        elif isinstance(item, scoretools.Tuplet) and rewrite_tuplets == False:
            pass
        else:
            #print('DESCENDING:', item)
            preprolated_duration = sum([x._preprolated_duration for x in item])
            if preprolated_duration.numerator == 1:
                preprolated_duration = mathtools.NonreducedFraction(
                    preprolated_duration)
                preprolated_duration = preprolated_duration.with_denominator(
                    preprolated_duration.denominator * 4)
            sub_metrical_hierarchy = metertools.Meter(preprolated_duration)
            sub_boundary_depth = 1
            if boundary_depth is None:
                sub_boundary_depth = None
            _rewrite_meter(
                item[:],
                sub_metrical_hierarchy,
                boundary_depth=sub_boundary_depth,
                maximum_dot_count=maximum_dot_count,
                )
