from abjad import *


def testMelodicObjectCounterpointInterval___init___01():

    mcpi = pitchtools.MelodicCounterpointInterval(15)

    assert repr(mcpi) == 'MelodicCounterpointInterval(+15)'
    assert str(mcpi) == '+15'
    assert mcpi.number == 15
