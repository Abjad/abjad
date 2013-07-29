from abjad import *


def test_ComponentSelection_attach_marks_01():

    staff = Staff("c'8 d'8 r8 f'8")
    selection = staff.select_notes_and_chords()
    selection = select(selection)
    articulations = [marktools.Articulation(x) for x in '^.']
    selection.attach_marks(articulations)

    r'''
    \new Staff {
        c'8 -\marcato -\staccato
        d'8 -\marcato -\staccato
        r8
        f'8 -\marcato -\staccato
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 -\\marcato -\\staccato\n\td'8 -\\marcato -\\staccato\n\tr8\n\tf'8 -\\marcato -\\staccato\n}"


def test_ComponentSelection_attach_marks_02():

    staff = Staff("c'8 d'8 r8 f'8")
    selection = staff.select_notes_and_chords()
    selection = select(selection)
    stem_tremolo = marktools.StemTremolo(16)
    selection.attach_marks(stem_tremolo)

    r'''
    \new Staff {
        c'8 :16
        d'8 :16
        r8
        f'8 :16
    }
    '''

    for leaf in staff.select_notes_and_chords():
        new_stem_tremolo = leaf.get_mark(marktools.StemTremolo)
        assert new_stem_tremolo == stem_tremolo
        assert new_stem_tremolo is not stem_tremolo

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 :16\n\td'8 :16\n\tr8\n\tf'8 :16\n}"
