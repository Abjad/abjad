# -*- coding: utf-8 -*-
import pytest
from abjad import *



@pytest.mark.skip('unskip me before building 2.15')
def test_topleveltools_play_01():
    r'''A note can be played.
    '''
    note = Note(1, (1, 2))
    play(note)


@pytest.mark.skip('unskip me before building 2.15')
def test_topleveltools_play_02():
    r'''A score can be played.
    '''
    notes = [Note(i, (1, 64)) for i in range(10)]
    score = Score([Staff(notes)])
    play(score)
