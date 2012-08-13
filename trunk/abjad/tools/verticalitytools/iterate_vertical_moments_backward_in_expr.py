from abjad.tools import componenttools


# TODO: optimize without multiple full-component traversal.
def iterate_vertical_moments_backward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate vertical moments backward in `expr`::

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

        
        >>> for x in verticalitytools.iterate_vertical_moments_backward_in_expr(score):
        ...     x.leaves
        ...
        (Note("b'8"), Note("g'4"), Note("c'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("f'8"))

    ::

        >>> for x in verticalitytools.iterate_vertical_moments_backward_in_expr(piano_staff):
        ...     x.leaves
        ...
        (Note("g'4"), Note("c'8"))
        (Note("g'4"), Note("d'8"))
        (Note("a'4"), Note("e'8"))
        (Note("a'4"), Note("f'8"))

    Return generator.
    '''
    from abjad.tools.verticalitytools.get_vertical_moment_at_offset_in_expr import \
        get_vertical_moment_at_offset_in_expr

    moments_in_governor = []
    for component in componenttools.iterate_components_forward_in_expr(expr):
        prolated_offset = component.start_offset
        if prolated_offset not in moments_in_governor:
            moments_in_governor.append(prolated_offset)
    moments_in_governor.sort()

    for moment_in_governor in reversed(moments_in_governor):
        yield get_vertical_moment_at_offset_in_expr(expr, moment_in_governor)
