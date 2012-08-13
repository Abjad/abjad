from abjad.tools import componenttools


# TODO: optimize without full-component traversal.
def get_vertical_moment_starting_with_component(component, governor=None):
    r'''.. versionadded:: 2.0

    Get vertical moment starting with `component`::

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

        >>> leaf = piano_staff[1][1]

    ::

        >>> verticalitytools.get_vertical_moment_starting_with_component(leaf)
        VerticalMoment(1/8, <<3>>)

    Get vertical moment starting with `component` in `governor` when
    `governor` is not none::

        >>> verticalitytools.get_vertical_moment_starting_with_component(leaf, 
        ... governor=piano_staff)
        VerticalMoment(1/8, <<2>>)

    Return vertical moment.
    '''
    from abjad.tools import verticalitytools

    prolated_offset = component.start_offset

    if governor is None:
        governor = componenttools.component_to_score_root(component)

    return verticalitytools.get_vertical_moment_at_offset_in_expr(governor, prolated_offset)
