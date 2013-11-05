# -*- encoding: utf-8 -*-
from abjad import *


# What's the best way to test play?

def test_functiontools_play_01():
    r'''A note can be played.
    '''
    note = Note(1, (1, 32))
    play(note)


def test_functiontools_play_02():
    r'''A score can be played.
    '''
    notes = [Note(i, (1, 64)) for i in range(10)]
    score = Score([Staff(notes)])
    play(score)
