from abjad import *


def test_componenttools_iterate_timeline_forward_from_component_01():
    '''Yield klass instances in score of expr,
    sorted by score offset and score index,
    and starting from expr.
    '''

    staff_1 = Staff(notetools.make_repeated_notes(4, Duration(1, 4)))
    staff_2 = Staff(notetools.make_repeated_notes(4, Duration(1, 8)))
    score_1 = Score([staff_1, staff_2])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score_1)

    r'''
    \new Score <<
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }
        \new Staff {
            g'8
            a'8
            b'8
            c''8
        }
    >>
    '''

    leaf_generator = componenttools.iterate_timeline_forward_from_component(staff_2[2])
    leaves = list(leaf_generator)

    assert leaves[0] is staff_2[2] # b'8
    assert leaves[1] is staff_2[3] # c''8
    assert leaves[2] is staff_1[2] # e'4
    assert leaves[3] is staff_1[3] # f'4


def test_componenttools_iterate_timeline_forward_from_component_02():
    '''Yield klass instances in score of expr,
    sorted by score offset and score index,
    and starting from expr.
    '''

    staff_1 = Staff(notetools.make_repeated_notes(4, Duration(1, 8)))
    staff_2 = Staff(notetools.make_repeated_notes(4, Duration(1, 4)))
    score = Score([staff_1, staff_2])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff {
            g'4
            a'4
            b'4
            c''4
        }
    >>
    '''

    leaf_generator = componenttools.iterate_timeline_forward_from_component(staff_1[3])
    leaves = list(leaf_generator)

    assert leaves[0] is staff_1[3] # f'8
    assert leaves[1] is staff_2[2] # b'4
    assert leaves[2] is staff_2[3] # c''4
