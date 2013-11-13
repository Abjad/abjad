# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMapping_name_01():

    mapping = pitchtools.OctaveTranspositionMapping()
    assert mapping.custom_identifier is None

    mapping.custom_identifier = 'lower register mapping #2'
    assert mapping.custom_identifier == 'lower register mapping #2'
