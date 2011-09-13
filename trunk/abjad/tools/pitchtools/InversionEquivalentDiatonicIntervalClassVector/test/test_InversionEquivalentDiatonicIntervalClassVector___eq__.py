from abjad import *


def test_InversionEquivalentDiatonicIntervalClassVector___eq___01():

    notes = notetools.make_notes([0, 2, 4], [(1, 4)])
    dicv1 = pitchtools.InversionEquivalentDiatonicIntervalClassVector(notes)

    notes = notetools.make_notes([5, 7, 9], [(1, 4)])
    dicv2 = pitchtools.InversionEquivalentDiatonicIntervalClassVector(notes)

    notes = notetools.make_notes([2, 4, 5], [(1, 4)])
    dicv3 = pitchtools.InversionEquivalentDiatonicIntervalClassVector(notes)


    assert dicv1 == dicv1
    assert dicv2 == dicv2
    assert dicv3 == dicv3
    assert dicv1 == dicv2
    assert not dicv1 == dicv3
    assert not dicv2 == dicv3
