from abjad import *


def test_leaftools_get_composite_offset_series_from_leaves_in_expr_01():

    staff_1 = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    staff_2 = Staff(notetools.make_repeated_notes(4))
    score = Score([staff_1, staff_2])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

    r'''
    \new Score <<
        \new Staff {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        \new Staff {
            b'8
            c''8
            d''8
            e''8
        }
    >>
    '''

    result = leaftools.get_composite_offset_series_from_leaves_in_expr(score)
    assert result == [Duration(0, 1), Duration(1, 12), Duration(1, 8), Duration(1, 6), Duration(1, 4), Duration(1, 3), Duration(3, 8), Duration(5, 12), Duration(1, 2)]
