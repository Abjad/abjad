# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_repeated_notes_01():
    r'''Allow nonassignable durations.
    '''

    t = Voice(notetools.make_repeated_notes(2, (5, 16)))

    r'''
    \new Voice {
        c'4 ~
        c'16
        c'4 ~
        c'16
    }
    '''

    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\tc'4 ~\n\tc'16\n\tc'4 ~\n\tc'16\n}"
        )
