from experimental import *


def test_pitch_01():
    '''Read from beginning.
    '''

    cursor = library.example_pitches_1()
    
    assert cursor() == [7]
    assert cursor() == [3]
    assert cursor() == [8]
    assert cursor() == [8]
    assert cursor() == [6]
    assert cursor(10) == [6, 4, 6, 10, 1, 8, 6, 10, 0, 1]


def test_pitch_02():
    '''Read from middle.
    '''

    cursor = library.example_pitches_1(position=(2, 0))

    assert cursor() == [18]
    assert cursor() == [17]
    assert cursor() == [17]
    assert cursor() == [19]
    assert cursor() == [14]
    assert cursor(10) == [18, 17, 18, 20, 21, 23, 14, 16, 12, 12]
