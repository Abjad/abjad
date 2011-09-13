from abjad import *


def test_pitchtools_set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr_01():
    '''Appictation works on tie chains.'''

    t = Voice(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        c'8 ~
        c'32
        cs'8 ~
        cs'32
        d'8 ~
        d'32
        ef'8 ~
        ef'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'32\n\tcs'8 ~\n\tcs'32\n\td'8 ~\n\td'32\n\tef'8 ~\n\tef'32\n}"
