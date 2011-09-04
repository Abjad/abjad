from abjad.tools.componenttools._Component import _Component
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr
from abjad.tools.verticalitytools.get_vertical_moment_at_prolated_offset_in_expr import get_vertical_moment_at_prolated_offset_in_expr
from abjad.tools import durationtools


def iterate_vertical_moments_backward_in_expr(governor):
    r'''.. versionadded:: 2.0

    Yield vertical moments forward in `governor`::

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
        abjad> for vertical_moment in verticalitytools.iterate_vertical_moments_backward_in_expr(score):
        ...     vertical_moment.leaves
        ...
        (Note("b'8"), Note("g'4"), Note("c'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("f'8"))
        abjad> for vertical_moment in verticalitytools.iterate_vertical_moments_backward_in_expr(piano_staff):
        ...     vertical_moment.leaves
        ...
        (Note("g'4"), Note("c'8"))
        (Note("g'4"), Note("d'8"))
        (Note("a'4"), Note("e'8"))
        (Note("a'4"), Note("f'8"))

    .. todo:: optimize without multiple full-component traversal.

    .. versionchanged:: 2.0
        renamed ``iterate.vertical_moments_backward_in()`` to
        ``verticalitytools.iterate_vertical_moments_backward_in_expr()``.

    .. versionchanged:: 2.0
        renamed ``iterate.vertical_moments_backward_in_expr()`` to
        ``verticalitytools.iterate_vertical_moments_backward_in_expr()``.
    '''
    from abjad.tools.verticalitytools.VerticalMoment import VerticalMoment

    moments_in_governor = []
    for component in iterate_components_forward_in_expr(governor, _Component):
        prolated_offset = component._offset.start
        if prolated_offset not in moments_in_governor:
            moments_in_governor.append(prolated_offset)
    moments_in_governor.sort()

    for moment_in_governor in reversed(moments_in_governor):
        yield get_vertical_moment_at_prolated_offset_in_expr(
            governor, moment_in_governor)
