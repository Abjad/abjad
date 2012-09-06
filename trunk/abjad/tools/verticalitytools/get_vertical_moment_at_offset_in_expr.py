from abjad.tools import componenttools


# TODO: optimize without full-component traversal.
def get_vertical_moment_at_offset_in_expr(expr, prolated_offset):
    r'''.. versionadded:: 2.0

    Get vertical moment at `prolated_offset` in `expr`::

        >>> from abjad.tools import verticalitytools

    ::

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
    from abjad.tools import verticalitytools

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
    governors.sort(lambda x, y: cmp(
            componenttools.component_to_score_index(x),
            componenttools.component_to_score_index(y)))
    governors = tuple(governors)

    components = []
    for governor in governors:
        for component in componenttools.iterate_components_forward_in_expr(governor):
            if component.start_offset <= prolated_offset:
                if prolated_offset < component.stop_offset:
                    components.append(component)
    components.sort(lambda x, y: cmp(
            componenttools.component_to_score_index(x),
            componenttools.component_to_score_index(y)))
    components = tuple(components)

    vertical_moment = verticalitytools.VerticalMoment(prolated_offset, governors, components)

    return vertical_moment
