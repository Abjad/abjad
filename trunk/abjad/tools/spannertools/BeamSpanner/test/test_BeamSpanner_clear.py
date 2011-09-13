from abjad import *


def test_BeamSpanner_clear_01():
    '''Clear length-one spanner.'''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])

    r'''
    \new Staff {
        c'8 []
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    spannertools.destroy_all_spanners_attached_to_component(t[0], spannertools.BeamSpanner)

    r'''
    \new Staff {
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_BeamSpanner_clear_02():
    '''Clear length-four spanner.'''

    t = Staff(notetools.make_repeated_notes(8))
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[:4])

    r'''
    \new Staff {
        c'8 []
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    spannertools.destroy_all_spanners_attached_to_component(t[0], spannertools.BeamSpanner)

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
