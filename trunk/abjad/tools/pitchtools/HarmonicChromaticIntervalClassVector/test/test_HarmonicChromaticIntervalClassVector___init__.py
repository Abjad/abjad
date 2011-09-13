from abjad import *


def test_HarmonicChromaticIntervalClassVector___init___01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
        g'8
    }
    '''

    CIV = pitchtools.HarmonicChromaticIntervalClassVector(staff)

    '''
    0 1 3 2 1 2 0 1 0 0 0 0
    '''

    assert CIV[0] == 0
    assert CIV[1] == 1
    assert CIV[2] == 3
    assert CIV[3] == 2
    assert CIV[4] == 1
    assert CIV[5] == 2
    assert CIV[6] == 0
    assert CIV[7] == 1
    assert CIV[8] == 0
    assert CIV[9] == 0
    assert CIV[10] == 0
    assert CIV[11] == 0
