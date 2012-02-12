from abjad.tools import durationtools


def is_bar_line_crossing_leaf(leaf):
    r'''.. versionadded:: 2.0

    True when `leaf` crosses bar line::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> t[2].written_duration *= 2
        abjad> contexttools.TimeSignatureMark((2, 8), partial = Duration(1, 8))(t[2])
        TimeSignatureMark((2, 8), partial = Duration(1, 8))(e'4)
        abjad> f(t)
        \new Staff {
            c'8
            d'8
            \partial 8
            \time 2/8
            e'4
            f'8
        }
        abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[2])
        True

    Otherwise false::

        abjad> leaftools.is_bar_line_crossing_leaf(t.leaves[3])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools
    from abjad.tools.durationtools import Duration

    meter = contexttools.get_effective_time_signature(leaf)

    if meter is None:
        meter_duration = Duration(4, 4)
    else:
        meter_duration = meter.duration

    partial = getattr(meter, 'partial', Duration(0))
    
    shifted_start = (leaf._offset.start - partial) % meter_duration

    if meter_duration < shifted_start + leaf.prolated_duration:
         return True

    return False
