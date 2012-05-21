from abjad import *


def testMelodicObjectDiatonicInterval___init___01():
    '''Init melodic diatonic interval from abbreviation.
    '''

    mdi = pitchtools.MelodicDiatonicInterval('+M3')
    assert mdi.quality_string == 'major'
    assert mdi.number == 3


def testMelodicObjectDiatonicInterval___init___02():
    '''Can init from quality string and interval number.'''

    mdi = pitchtools.MelodicDiatonicInterval('major', 3)
    assert mdi.quality_string == 'major'
    assert mdi.number == 3


def testMelodicObjectDiatonicInterval___init___03():
    '''Can init from other melodic diatonic interval instance.'''

    mdi = pitchtools.MelodicDiatonicInterval('major', 3)
    new = pitchtools.MelodicDiatonicInterval(mdi)

    assert mdi.quality_string == 'major'
    assert mdi.number == 3

    assert new.quality_string == 'major'
    assert new.number == 3

    assert new is not mdi
    assert new == mdi
