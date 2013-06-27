from abjad import *


def test_BeamSpanner_clear_01():
    '''Clear length-one spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[0])

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

    spannertools.destroy_spanners_attached_to_component(
        staff[0], beamtools.BeamSpanner)

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

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_BeamSpanner_clear_02():
    '''Clear length-four spanner.
    '''

    staff = Staff(notetools.make_repeated_notes(8))
    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:4])

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    spannertools.destroy_spanners_attached_to_component(
        staff[0], beamtools.BeamSpanner)

    assert wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
