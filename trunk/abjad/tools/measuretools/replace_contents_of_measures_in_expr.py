from abjad.tools.measuretools.Measure import Measure
from abjad.tools import contexttools
from abjad.tools.measuretools.append_spacer_skips_to_underfull_measures_in_expr import append_spacer_skips_to_underfull_measures_in_expr
from abjad.tools.measuretools.get_next_measure_from_component import get_next_measure_from_component


# TODO: fix bug in function that causes tied notes to become untied
def replace_contents_of_measures_in_expr(expr, new_contents):
    r'''.. versionadded:: 1.1

    Replace contents of measures in `expr` with `new_contents`::

        abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (3, 16)]))

    ::

        abjad> f(staff)
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

        abjad> notes = [Note("c'16"), Note("d'16"), Note("e'16"), Note("f'16")]
        abjad> measuretools.replace_contents_of_measures_in_expr(staff, notes)
        [Measure(1/8, [c'16, d'16]), Measure(3/16, [e'16, f'16, s1 * 1/16])]

    ::

        abjad> f(staff)
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

    Preserve duration of all measures.

    Skip measures that are too small.

    Pad extra space at end of measures with spacer skip.

    If not enough measures raise stop iteration.

    Return measures iterated.

    .. versionchanged:: 2.0
        renamed ``measuretools.overwrite_contents()`` to
        ``measuretools.replace_contents_of_measures_in_expr()``.
    '''

    # init return list
    result = []

    # get first measure and first meter
    cur_measure = get_next_measure_from_component(expr)
    result.append(cur_measure)
    cur_meter = contexttools.get_effective_time_signature(cur_measure)
    del(cur_measure[:])

    # iterate new contents
    while new_contents:

        # find candidate duration of new element plus current measure
        cur_element = new_contents[0]
        multiplier = cur_meter.multiplier
        preprolated_duration = cur_element.preprolated_duration
        prolated_duration = multiplier * preprolated_duration
        candidate_duration = cur_measure.prolated_duration + prolated_duration

        # if new element fits in current measure
        if candidate_duration <= cur_meter.duration:
            cur_element = new_contents.pop(0)
            cur_measure.append(cur_element)

        # otherwise restore currene measure and advance to next measure
        else:
            cur_meter = contexttools.TimeSignatureMark(cur_meter)
            contexttools.detach_time_signature_marks_attached_to_component(cur_measure)
            cur_meter.attach(cur_measure)
            append_spacer_skips_to_underfull_measures_in_expr([cur_measure])
            cur_measure = get_next_measure_from_component(cur_measure)
            if cur_measure is None:
                raise StopIteration
            result.append(cur_measure)
            cur_meter = contexttools.get_effective_time_signature(cur_measure)
            del(cur_measure[:])

    # restore last iterated measure
    cur_meter = contexttools.TimeSignatureMark(cur_meter)
    contexttools.detach_time_signature_marks_attached_to_component(cur_measure)
    cur_meter.attach(cur_measure)
    append_spacer_skips_to_underfull_measures_in_expr(cur_measure)

    # return iterated measures
    return result
