from abjad.tools.componenttools.component_to_score_root import component_to_score_root
from abjad.tools.verticalitytools.get_vertical_moment_at_prolated_offset_in_expr import get_vertical_moment_at_prolated_offset_in_expr


def get_vertical_moment_starting_with_component(expr, governor = None):
    r'''.. versionadded:: 2.0

    When `governor` is none, get vertical moment at
    ``expr._offset.start`` in score root of `expr`::

        abjad> from abjad.tools import verticalitytools

    ::

        abjad> score = Score([])
        abjad> score.append(Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))]))
        abjad> piano_staff = scoretools.PianoStaff([])
        abjad> piano_staff.append(Staff(notetools.make_repeated_notes(2, Duration(1, 4))))
        abjad> piano_staff.append(Staff(notetools.make_repeated_notes(4)))
        abjad> contexttools.ClefMark('bass')(piano_staff[1])
        ClefMark('bass')(Staff{4})
        abjad> score.append(piano_staff)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(list(reversed(score.leaves)))
        abjad> f(score)
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
        abjad> verticalitytools.get_vertical_moment_starting_with_component(piano_staff[1][1])
        VerticalMoment(1/8, <<3>>)

    When `governor` is not none, get vertical moment at
    ``expr._offset.start`` in `governor`. ::

        abjad> verticalitytools.get_vertical_moment_starting_with_component(piano_staff[1][1], piano_staff)
        VerticalMoment(1/8, <<2>>)

    .. todo:: optimize without full-component traversal.

    .. versionchanged:: 2.0
        renamed ``iterate.get_vertical_moment_starting_with()`` to
        ``verticalitytools.get_vertical_moment_starting_with_component()``.

    .. versionchanged:: 2.0
        renamed ``iterate.get_vertical_moment_starting_with_component()`` to
        ``verticalitytools.get_vertical_moment_starting_with_component()``.
    '''

    prolated_offset = expr._offset.start

    if governor is None:
        governor = component_to_score_root(expr)

    return get_vertical_moment_at_prolated_offset_in_expr(governor, prolated_offset)
