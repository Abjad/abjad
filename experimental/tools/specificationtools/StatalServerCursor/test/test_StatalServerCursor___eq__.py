from experimental import *


def test_StatalServerCursor___eq___01():

    cursor_1 = library.example_pitches_1()
    cursor_2 = library.example_pitches_1()

    assert cursor_1 == cursor_1
    assert cursor_1 == cursor_2
    assert cursor_2 == cursor_1
    assert cursor_2 == cursor_2


def test_StatalServerCursor___eq___02():

    cursor_1 = library.example_pitches_1()
    cursor_2 = library.example_pitches_1()
    cursor_1()
    
    assert     cursor_1 == cursor_1
    assert not cursor_1 == cursor_2
    assert not cursor_2 == cursor_1
    assert     cursor_2 == cursor_2
