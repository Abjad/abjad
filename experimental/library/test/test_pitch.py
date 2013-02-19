from experimental import *


def test_pitch_01():
    '''Read from beginning.
    '''

    cursor = library.example_pitches_1()
    
    assert cursor() == [0]
    assert cursor() == [1]
    assert cursor() == [2]
    assert cursor() == [3]
    assert cursor() == [4]
    assert cursor(10) == [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


def test_pitch_02():
    '''Read from middle.
    '''

    cursor = library.example_pitches_1(position=(2, 0))

    assert cursor() == [13]
    assert cursor() == [14]
    assert cursor() == [15]
    assert cursor() == [16]
    assert cursor() == [17]
    assert cursor(10) == [18, 19, 20, 21, 22, 23, 0, 1, 2, 3]
