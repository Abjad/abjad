from abjad import *


def testNumberedObjectChromaticPitchClassSet___hash___01():
    '''Pitch class sets are hashable.'''

    pcset = pitchtools.NumberedChromaticPitchClassSet([0, 1, 2])

    assert hash(pcset) == hash(repr(pcset))
