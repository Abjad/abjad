# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_repeated_notes_01():
    r'''Allow nonassignable durations.
    '''

    voice = Voice(scoretools.make_repeated_notes(2, (5, 16)))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'4 ~
            c'16
            c'4 ~
            c'16
        }
        '''
        )
