from abjad import *


def test_MelodicChromaticIntervalClassVector___str___01():

    numbers = [-24, -24, -12, -12, -6, -5, 0, 0, 1, 9, 9, 9, 12]
    mcicvector = pitchtools.MelodicChromaticIntervalClassVector(numbers)

    '''
        2   |   1   .   .   .   .   .   |   .   .   3   .   .   1
            |   .   .   .   .   1   1   |   .   .   .   .   .   4
            |   .   .   .   .   .   .   |   .   .   .   .   .   .
            |   .   .   .   .   .   .   |   .   .   .   .   .   .
    '''

    assert str(mcicvector) == '  2   |   1   .   .   .   .   .   |   .   .   3   .   .   1\n      |   .   .   .   .   1   1   |   .   .   .   .   .   4\n      |   .   .   .   .   .   .   |   .   .   .   .   .   .\n      |   .   .   .   .   .   .   |   .   .   .   .   .   .'
