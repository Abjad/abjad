from abjad import *


def test_Scale_make_notes_01():
    '''Allow nonassignable durations.
    '''

    scale = tonalitytools.Scale('c', 'major')
    notes = scale.make_notes(2, Duration(5, 16))
    staff = Staff(notes)

    r'''
    \new Staff {
        c'4 ~
        c'16
        d'4 ~
        d'16
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'4 ~\n\tc'16\n\td'4 ~\n\td'16\n}"
