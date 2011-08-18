from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_make_first_n_notes_in_ascending_diatonic_scale_01():
    '''Allow nonassignable durations.'''

    t = Staff(tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(2, (5, 16)))

    r'''
    \new Staff {
        c'4 ~
        c'16
        d'4 ~
        d'16
    }
    '''

    assert t.format == "\\new Staff {\n\tc'4 ~\n\tc'16\n\td'4 ~\n\td'16\n}"
