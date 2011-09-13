from abjad.tools import mathtools
from abjad.tools.leaftools.get_composite_offset_series_from_leaves_in_expr import get_composite_offset_series_from_leaves_in_expr


def get_composite_offset_difference_series_from_leaves_in_expr(expr):
    r'''.. versionadded:: 2.0

    Get composite offset difference series from leaves in `expr`::

        abjad> staff_1 = Staff([tuplettools.FixedDurationTuplet(Duration(4, 8), notetools.make_repeated_notes(3))])
        abjad> staff_2 = Staff(notetools.make_repeated_notes(4))
        abjad> score = Score([staff_1, staff_2])
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)
        abjad> f(score)
            \new Score <<
                \new Staff {
                    \fraction \times 4/3 {
                        c'8
                        d'8
                        e'8
                    }
                }
                \new Staff {
                    f'8
                    g'8
                    a'8
                    b'8
                }
            >>
        abjad> leaftools.get_composite_offset_difference_series_from_leaves_in_expr(score)
        [Offset(1, 8), Offset(1, 24), Offset(1, 12), Offset(1, 12), Offset(1, 24), Offset(1, 8)]

    Composite offset difference series defined equal to time intervals between
    unique start and stop offsets of leaves in `expr`.

    Return list of fractions.
    '''

    return list(mathtools.difference_series(get_composite_offset_series_from_leaves_in_expr(expr)))
