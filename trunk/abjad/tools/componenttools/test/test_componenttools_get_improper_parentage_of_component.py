from abjad import *


def test_componenttools_get_improper_parentage_of_component_01():
    '''t._parentage.improper_parentage returns a list of the elements
    in the parentage of t, including t.
    '''

    t = Score([Staff(Container(notetools.make_repeated_notes(2)) * 2)])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Score <<
        \new Staff {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
    >>
    '''

    improper_parentage = componenttools.get_improper_parentage_of_component(t.leaves[0])

    "[Note(c', 8), Container(c'8, d'8), Staff{2}, Score<<1>>]"

    assert len(improper_parentage) == 4
    assert improper_parentage[0] is t[0][0][0]
    assert improper_parentage[1] is t[0][0]
    assert improper_parentage[2] is t[0]
    assert improper_parentage[3] is t


def test_componenttools_get_improper_parentage_of_component_02():
    '''t._parentage.improper_parentage returns a list of the elements
        in the parentage of container t, including t.'''

    t = Score([Staff(Container(notetools.make_repeated_notes(2)) * 2)])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Score <<
        \new Staff {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
    >>
    '''

    improper_parentage = componenttools.get_improper_parentage_of_component(t[0][0])

    "[Container(c'8, d'8), Staff{2}, Score<<1>>]"

    assert len(improper_parentage) == 3
    assert improper_parentage[0] is t[0][0]
    assert improper_parentage[1] is t[0]
    assert improper_parentage[2] is t
