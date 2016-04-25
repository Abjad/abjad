# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Chord___repr___01():
    r'''Chord repr is evaluable.
    '''

    chord_1 = Chord("<ef' cs'' f''>4")
    chord_2 = eval(repr(chord_1))

    assert isinstance(chord_1, Chord)
    assert isinstance(chord_2, Chord)
    assert format(chord_1) == format(chord_2)
    assert chord_1 is not chord_2


def test_scoretools_Chord___repr___02():
    '''Chord repr works with forced and cautionary accidentals.
    '''

    chord = Chord('<c! e? g!? b>4')
    assert "Chord('{}')".format(format(chord)) == repr(chord)
