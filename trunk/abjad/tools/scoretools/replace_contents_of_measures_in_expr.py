# -*- encoding: utf-8 -*-


# TODO: fix bug in function that causes tied notes to become untied
def replace_contents_of_measures_in_expr(expr, new_contents):
    r'''Replaces contents of measures in `expr` with `new_contents`.

    ..  container:: example

        **Example.**

        ::

            >>> staff = Staff(scoretools.make_measures_with_full_measure_spacer_skips(
            ...     [(1, 8), (3, 16)]))
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 1/8
                    s1 * 1/8
                }
                {
                    \time 3/16
                    s1 * 3/16
                }
            }

        ::

            >>> notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
            >>> scoretools.replace_contents_of_measures_in_expr(staff, notes)
            [Measure(1/8, [c'16, d'16]), Measure(3/16, [e'16, f'16, s1 * 1/16])]
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 1/8
                    c'16
                    d'16
                }
                {
                    \time 3/16
                    e'16
                    f'16
                    s1 * 1/16
                }
            }

    Preserves duration of all measures.

    Skips measures that are too small.

    Pads extra space at end of measures with spacer skip.

    Raises stop iteration if not enough measures.

    Returns measures iterated.
    '''
    from abjad.tools import marktools
    from abjad.tools import scoretools
    from abjad.tools.functiontools import attach

    # init return list
    result = []

    # get first measure and first time signature
    current_measure = scoretools.get_next_measure_from_component(expr)
    result.append(current_measure)
    current_time_signature = current_measure.time_signature
    # to avoide pychecker slice assignment error
    #del(current_measure[:])
    current_measure.__delitem__(slice(0, len(current_measure)))

    # iterate new contents
    while new_contents:

        # find candidate duration of new element plus current measure
        current_element = new_contents[0]
        multiplier = current_time_signature.implied_prolation
        preprolated_duration = current_element._preprolated_duration
        duration = multiplier * preprolated_duration
        candidate_duration = current_measure._get_duration() + duration

        # if new element fits in current measure
        if candidate_duration <= current_time_signature.duration:
            current_element = new_contents.pop(0)
            current_measure._append_without_withdrawing_from_crossing_spanners(
                current_element)

        # otherwise restore current measure and advance to next measure
        else:
            current_time_signature = \
                marktools.TimeSignatureMark(current_time_signature)
            for mark in current_measure._get_marks(
                marktools.TimeSignatureMark):
                mark.detach()
            attach(current_time_signature, current_measure)
            scoretools.append_spacer_skips_to_underfull_measures_in_expr(
                [current_measure])
            current_measure = scoretools.get_next_measure_from_component(
                current_measure)
            if current_measure is None:
                raise StopIteration
            result.append(current_measure)
            current_time_signature = current_measure.time_signature
            # to avoid pychecker slice assignment error
            #del(current_measure[:])
            current_measure.__delitem__(slice(0, len(current_measure)))

    # restore last iterated measure
    current_time_signature = \
        marktools.TimeSignatureMark(current_time_signature)
    for mark in current_measure._get_marks(marktools.TimeSignatureMark):
        mark.detach()
    attach(current_time_signature, current_measure)
    scoretools.append_spacer_skips_to_underfull_measures_in_expr(
        current_measure)

    # return iterated measures
    return result
