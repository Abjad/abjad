from abjad import *


def test_marktools_attach_stem_tremolos_to_notes_and_chords_in_expr_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    stem_tremolo = marktools.StemTremolo(16)
    marktools.attach_stem_tremolos_to_notes_and_chords_in_expr(staff, [stem_tremolo])

    r'''
    \new Staff {
        c'8 :16
        d'8 :16
        e'8 :16
        f'8 :16
    }
    '''

    for leaf in staff.leaves:
        new_stem_tremolo = marktools.get_stem_tremolo_attached_to_component(leaf)
        assert new_stem_tremolo == stem_tremolo
        assert new_stem_tremolo is not stem_tremolo

    assert staff.format == "\\new Staff {\n\tc'8 :16\n\td'8 :16\n\te'8 :16\n\tf'8 :16\n}"
