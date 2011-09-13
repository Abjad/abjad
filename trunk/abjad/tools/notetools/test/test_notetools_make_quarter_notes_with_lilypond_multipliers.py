from abjad import *


def test_notetools_make_quarter_notes_with_lilypond_multipliers_01():

    multipliers = [(1, 4), (1, 5), (1, 6), (1, 7)]
    notes = notetools.make_quarter_notes_with_lilypond_multipliers([0], multipliers)
    t = Staff(notes)

    r'''
    \new Staff {
        c'4 * 1
        c'4 * 4/5
        c'4 * 2/3
        c'4 * 4/7
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'4 * 1\n\tc'4 * 4/5\n\tc'4 * 2/3\n\tc'4 * 4/7\n}"
