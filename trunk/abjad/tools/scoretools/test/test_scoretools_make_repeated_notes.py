# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_repeated_notes_01():
    r'''Allow nonassignable durations.
    '''

    voice = Voice(scoretools.make_repeated_notes(2, (5, 16)))

    r'''
    \new Voice {
        c'4 ~
        c'16
        c'4 ~
        c'16
    }
    '''

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'4 ~
            c'16
            c'4 ~
            c'16
        }
        '''
        )
