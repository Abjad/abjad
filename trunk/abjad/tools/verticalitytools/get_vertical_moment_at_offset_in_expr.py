from abjad.tools import componenttools
from abjad.tools import durationtools


# TODO: optimize without full-component traversal.
def get_vertical_moment_at_offset_in_expr(expr, offset):
    r'''.. versionadded:: 2.0

    Get vertical moment at `offset` in `expr`::

        >>> score = Score([])
        >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
        >>> score.append(staff)

    ::

        >>> piano_staff = scoretools.PianoStaff([])
        >>> piano_staff.append(Staff("a'4 g'4"))
        >>> piano_staff.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
        >>> score.append(piano_staff)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                \fraction \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>

    ::

        >>> args = (piano_staff, durationtools.Offset(1, 8))

    ::

        >>> verticalitytools.get_vertical_moment_at_offset_in_expr(*args)
        VerticalMoment(1/8, <<2>>)

    ::

        >>> vertical_moment = _
        >>> vertical_moment.leaves
        (Note("a'4"), Note("e'8"))

    Return vertical moment.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import verticalitytools

    def find_index(container, offset):
        '''Based off of Python's bisect.bisect() function.'''
        lo = 0
        hi = len(container)
        while lo < hi:
            mid = (lo + hi) // 2
            start_offset = container[mid].timespan.start_offset
            stop_offset = container[mid].timespan.stop_offset
            if start_offset <= offset < stop_offset:
                lo = mid + 1
            elif start_offset < stop_offset: # if container[mid] is of non-zero duration
                hi = mid
            else: # else, container[mid] _is_ of zero duration, so we skip it
                lo = mid + 1
        return lo - 1

    def recurse(component, offset):
        result = []
        if component.timespan.start_offset <= offset < component.timespan.stop_offset:
            result.append(component)
            if hasattr(component, '_music'):
                if component.is_parallel:
                    for x in component:
                        result.extend(recurse(x, offset))
                else:
                    child = component[find_index(component, offset)]
                    result.extend(recurse(child, offset))
        return result

    offset = durationtools.Offset(offset)

    governors = []
    message = 'must be Abjad component or list or tuple of Abjad components.'
    if isinstance(expr, componenttools.Component):
        governors.append(expr)
    elif isinstance(expr, (list, tuple)):
        for x in expr:
            if isinstance(x, componenttools.Component):
                governors.append(x)
            else:
                raise TypeError(message)
    else:
        raise TypeError(message)
    governors.sort(lambda x, y: cmp(x.parentage.score_index, y.parentage.score_index))
    governors = tuple(governors)

    components = []
    for governor in governors:
        components.extend(recurse(governor, offset))
    components.sort(lambda x, y: cmp(x.parentage.score_index, y.parentage.score_index))
    components = tuple(components)

    vertical_moment = verticalitytools.VerticalMoment(offset, governors, components)

    return vertical_moment
