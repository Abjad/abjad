# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitchClassSegment


def test_NamedPitchClassSegment___repr___01():
    r'''Named chromatic pitch-class segment repr is evaluable.
    '''

    ncpcs = ['gs', 'a', 'as', 'c', 'cs']
    named_chromatic_pitch_class_segment_1 = pitchtools.NamedPitchClassSegment(ncpcs)
    named_chromatic_pitch_class_segment_2 = eval(repr(named_chromatic_pitch_class_segment_1))

    assert isinstance(named_chromatic_pitch_class_segment_1, NamedPitchClassSegment)
    assert isinstance(named_chromatic_pitch_class_segment_2, NamedPitchClassSegment)
