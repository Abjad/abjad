from abjad import *


def test_InversionEquivalentChromaticIntervalClassVector___init___01():
    '''Init inversion-equivalent chromatic interval-class vector from list of numbers.
    '''

    iecicv = pitchtools.InversionEquivalentChromaticIntervalClassVector([1, 1, 6, 2, 2, 2])

    assert sorted(iecicv.items()) == [
        (0, 0), (0.5, 0), (1, 2), (1.5, 0), (2, 3), (2.5, 0), (3, 0), (3.5, 0),
        (4, 0), (4.5, 0), (5, 0), (5.5, 0), (6, 1)]


def test_InversionEquivalentChromaticIntervalClassVector___init___02():
    '''Init inversion-equivalent chromatic interval-class vector from interval-class counts.
    '''

    iecicv = pitchtools.InversionEquivalentChromaticIntervalClassVector(
        counts = [2, 3, 0, 0, 0, 1])

    assert sorted(iecicv.items()) == [
        (0, 0), (0.5, 0), (1, 2), (1.5, 0), (2, 3), (2.5, 0), (3, 0), (3.5, 0),
        (4, 0), (4.5, 0), (5, 0), (5.5, 0), (6, 1)]
