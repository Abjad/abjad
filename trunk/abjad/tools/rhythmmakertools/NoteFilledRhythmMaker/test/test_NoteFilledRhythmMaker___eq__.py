from abjad import *


def test_NoteFilledRhythmMaker___eq___01():

    maker_1 = rhythmmakertools.NoteFilledRhythmMaker()
    maker_2 = rhythmmakertools.NoteFilledRhythmMaker()

    assert maker_1 == maker_2
    assert maker_2 == maker_1
    assert not maker_1 == 'foo'
