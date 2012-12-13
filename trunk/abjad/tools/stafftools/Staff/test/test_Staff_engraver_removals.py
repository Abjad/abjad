from abjad import *


def test_Staff_engraver_removals_01():

    t = Staff("c'8 d'8 e'8 f'8")
    t.engraver_removals.append('Time_signature_engraver')
    t.engraver_removals.append('Bar_number_engraver')

    r'''
    \new Staff \with {
        \remove Time_signature_engraver
        \remove Bar_number_engraver
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff \\with {\n\t\\remove Time_signature_engraver\n\t\\remove Bar_number_engraver\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
