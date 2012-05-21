from abjad import *
import py.test


def testMelodicObjectCounterpointInterval_semitones_01():
    '''Counterpint intervals evaluate to no exact number of semitones.'''

    mcpi = pitchtools.MelodicCounterpointInterval(15)

    assert py.test.raises(NotImplementedError, 'mcpi.semitones')
