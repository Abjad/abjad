from abjad import *


def test_pitchtools_set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr_01():
    '''Diatonicize notes in staff.'''

    t = Staff(notetools.make_repeated_notes(4))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_pitchtools_set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr_02():
    '''Diatonicize tie chains in staff.'''

    t = Staff(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        c'8 ~
        c'32
        d'8 ~
        d'32
        e'8 ~
        e'32
        f'8 ~
        f'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"


def test_pitchtools_set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr_03():
    '''Diatonicize tie chains in staff according to key signature.'''

    t = Staff(notetools.make_notes(0, [(5, 32)] * 4))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t, contexttools.KeySignatureMark('fs', 'major'))

    r'''
    \new Staff {
        fs'8 ~
        fs'32
        gs'8 ~
        gs'32
        as'8 ~
        as'32
        b'8 ~
        b'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tfs'8 ~\n\tfs'32\n\tgs'8 ~\n\tgs'32\n\tas'8 ~\n\tas'32\n\tb'8 ~\n\tb'32\n}"
