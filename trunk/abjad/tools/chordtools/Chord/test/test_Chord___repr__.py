from abjad import *


def test_Chord___repr___01():
    '''Chord repr is evaluable.
    '''

    chord_1 = Chord([3, 13, 17], (1, 4))
    chord_2 = eval(repr(chord_1))

    assert isinstance(chord_1, Chord)
    assert isinstance(chord_2, Chord)
    assert chord_1.lilypond_format == chord_2.lilypond_format
    assert chord_1 is not chord_2


def test_Chord___repr___02():
    chord = Chord('<c! e? g!? b>4')
    assert "Chord('{}')".format(chord.lilypond_format) == repr(chord)
