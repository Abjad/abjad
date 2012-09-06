from abjad.tools import containertools


def fuse_contiguous_measures_in_container_cyclically_by_counts(container, counts, mark=False):
    r'''.. versionadded:: 1.1

    Fuse contiguous measures in `container` cyclically by `counts`::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 5)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
            {
                d''8
                e''8
            }
        }

    ::

        >>> counts = (2, 1)
        >>> measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts(staff, counts)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 4/8
                c'8
                d'8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
            {
                \time 4/8
                b'8
                c''8
                d''8
                e''8
            }
        }

    Return none.

    Set `mark` to true to mark fused measures for later reference.

    .. versionchanged:: 2.0
        renamed ``fuse.measures_by_counts_cyclic()`` to
        ``measuretools.fuse_contiguous_measures_in_container_cyclically_by_counts()``.
    '''
    from abjad.tools import contexttools
    from abjad.tools import markuptools
    from abjad.tools import measuretools

    assert isinstance(container, containertools.Container)
    assert isinstance(counts, (tuple, list))

    try:
        container._update_marks_of_entire_score_tree_if_necessary()
        container._forbid_component_update()
        len_parts = len(counts)
        part_index = 0
        cur_measure = measuretools.get_next_measure_from_component(container)
        while True:
            part_count = counts[part_index % len_parts]
            if 1 < part_count:
                measures_to_fuse = []
                measure_to_fuse = cur_measure
                for x in range(part_count):
                    measures_to_fuse.append(measure_to_fuse)
                    measure_to_fuse = measuretools.get_next_measure_from_component(measure_to_fuse)
                    if measure_to_fuse is None:
                        break
                meter_sum_str = ' + '.join([
                    str(contexttools.get_effective_time_signature(x)) for x in measures_to_fuse])
                meter_sum_str = '"%s"' % meter_sum_str
                new = measuretools.fuse_measures(measures_to_fuse)
                if mark:
                    markuptools.Markup(meter_sum_str, Up)(new.leaves[0])
                cur_measure = new
            cur_measure = measuretools.get_next_measure_from_component(cur_measure)
            if cur_measure is None:
                break
            part_index += 1
    finally:
        container._allow_component_update()
