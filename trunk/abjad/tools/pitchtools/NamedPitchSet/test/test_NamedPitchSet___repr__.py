# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitchSet


def test_NamedPitchSet___repr___01():
    r'''Named chromatic pitch set repr is evaluable.
    '''

    ncps =['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_set_1 = pitchtools.NamedPitchSet(ncps)
    named_chromatic_pitch_set_2 = eval(repr(named_chromatic_pitch_set_1))

    assert isinstance(named_chromatic_pitch_set_1, pitchtools.NamedPitchSet)
    assert isinstance(named_chromatic_pitch_set_2, pitchtools.NamedPitchSet)
