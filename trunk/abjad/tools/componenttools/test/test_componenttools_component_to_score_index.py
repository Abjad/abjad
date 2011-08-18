from abjad import *


def test_componenttools_component_to_score_index_01():
    '''Exact numeric location of component in score as
    a tuple of zero or more nonnegative integers.
    '''

    staff_1 = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    staff_2 = Staff([tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3))])
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
            \times 2/3 {
                b'8
                c''8
                d''8
            }
        }
    >>
    '''

    #indices = [leaf.score.index for leaf in score.leaves]
    indices = [componenttools.component_to_score_index(leaf) for leaf in score.leaves]

    assert indices[0] == (0, 0, 0)
    assert indices[1] == (0, 0, 1)
    assert indices[2] == (0, 0, 2)
    assert indices[3] == (0, 1, 0)
    assert indices[4] == (0, 1, 1)
    assert indices[5] == (0, 1, 2)
    assert indices[6] == (1, 0, 0)
    assert indices[7] == (1, 0, 1)
    assert indices[8] == (1, 0, 2)
