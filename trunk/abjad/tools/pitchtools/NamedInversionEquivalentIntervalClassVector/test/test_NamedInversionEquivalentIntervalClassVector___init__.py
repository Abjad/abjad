# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInversionEquivalentIntervalClassVector___init___01():

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    dicv = pitchtools.NamedInversionEquivalentIntervalClassVector(notes)

    assert dicv[pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)] == 1
    assert dicv[pitchtools.NamedInversionEquivalentIntervalClass('major', 2)] == 2
    assert dicv[pitchtools.NamedInversionEquivalentIntervalClass('minor', 3)] == 1
    assert dicv[pitchtools.NamedInversionEquivalentIntervalClass('major', 3)] == 1
    assert dicv[pitchtools.NamedInversionEquivalentIntervalClass('perfect', 4)] == 1
