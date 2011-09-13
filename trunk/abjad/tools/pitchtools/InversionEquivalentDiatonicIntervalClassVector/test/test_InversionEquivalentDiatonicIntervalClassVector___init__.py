from abjad import *


def test_InversionEquivalentDiatonicIntervalClassVector___init___01():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    dicv = pitchtools.InversionEquivalentDiatonicIntervalClassVector(notes)

    assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)] == 1
    assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)] == 2
    assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3)] == 1
    assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)] == 1
    assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 4)] == 1
