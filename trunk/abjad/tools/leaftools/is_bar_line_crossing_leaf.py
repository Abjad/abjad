from abjad.tools import durationtools


def is_bar_line_crossing_leaf(leaf):
    r'''.. versionadded:: 2.0

    True when `leaf` crosses bar line::

        >>> t = Staff("c'8 d'8 e'8 f'8")
        >>> t[2].written_duration *= 2
        >>> contexttools.TimeSignatureMark((2, 8), partial = Duration(1, 8))(t[2])
        TimeSignatureMark((2, 8), partial=Duration(1, 8))(e'4)
        >>> f(t)
        \new Staff {
            c'8
            d'8
            \partial 8
            \time 2/8
            e'4
            f'8
        }
        >>> leaftools.is_bar_line_crossing_leaf(t.leaves[2])
        True

    Otherwise false::

        >>> leaftools.is_bar_line_crossing_leaf(t.leaves[3])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    time_signature = contexttools.get_effective_time_signature(leaf)

    if time_signature is None:
        time_signature_duration = durationtools.Duration(4, 4)
    else:
        time_signature_duration = time_signature.duration

    partial = getattr(time_signature, 'partial', durationtools.Duration(0))
    
    shifted_start = (leaf.start_offset - partial) % time_signature_duration

    if time_signature_duration < shifted_start + leaf.prolated_duration:
         return True

    return False
