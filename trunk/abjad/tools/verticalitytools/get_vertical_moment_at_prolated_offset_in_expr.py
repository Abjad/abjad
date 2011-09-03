from abjad.tools.componenttools._Component import _Component
from abjad.tools import componenttools
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def get_vertical_moment_at_prolated_offset_in_expr(governor, prolated_offset):
    r'''.. versionadded:: 2.0

    Get vertical moment at `prolated_offset` in `governor`::

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
        abjad> vertical_moment = verticalitytools.get_vertical_moment_at_prolated_offset_in_expr(piano_staff, Duration(1, 8))
        abjad> vertical_moment.leaves
        (Note("a'4"), Note("e'8"))

    .. todo:: optimize without full-component traversal.

    .. versionchanged:: 2.0
        renamed ``iterate.get_vertical_moment_at_prolated_offset_in()`` to
        ``verticalitytools.get_vertical_moment_at_prolated_offset_in_expr()``.
    '''
    from abjad.tools.verticalitytools.VerticalMoment import VerticalMoment

    governors = []
    message = 'must be Abjad component or list or tuple of Abjad components.'
    if isinstance(governor, _Component):
        governors.append(governor)
    elif isinstance(governor, (list, tuple)):
        for x in governor:
            if isinstance(x, _Component):
                governors.append(x)
            else:
                raise TypeError(message)
    else:
        raise TypeError(message)
    #governors.sort(lambda x, y: cmp(x.score.index, y.score.index))
    governors.sort(lambda x, y: cmp(
            componenttools.component_to_score_index(x),
            componenttools.component_to_score_index(y)))
    governors = tuple(governors)

    components = []
    for governor in governors:
        for component in iterate_components_forward_in_expr(governor, _Component):
            if component._offset.start <= prolated_offset:
                if prolated_offset < component._offset.stop:
                    components.append(component)
    #components.sort(lambda x, y: cmp(x.score.index, y.score.index))
    components.sort(lambda x, y: cmp(
            componenttools.component_to_score_index(x),
            componenttools.component_to_score_index(y)))
    components = tuple(components)

    vertical_moment = VerticalMoment(prolated_offset, governors, components)

    return vertical_moment
