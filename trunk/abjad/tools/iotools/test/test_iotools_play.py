# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import iotools


# What's the best way to test play?

def test_iotools_play_01():
    r'''A note can be played.
    '''
    n = Note(1, (1, 32))
    play(n)


def test_iotools_play_02():
    r'''A score can be played.
    '''
    notes = [Note(i, (1, 64)) for i in range(10)]
    score = Score([Staff(notes)])
    play(score)
