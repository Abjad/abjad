from abjad import *


def test_NoteFilledTimeTokenMaker___eq___01():

    maker_1 = timetokentools.NoteFilledTimeTokenMaker()
    maker_2 = timetokentools.NoteFilledTimeTokenMaker()

    assert maker_1 == maker_2
    assert maker_2 == maker_1
    assert not maker_1 == 'foo'
