# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionmapping_custom_identifier_01():

    mapping = pitchtools.OctaveTranspositionMapping()
    assert mapping.custom_identifier is None

    mapping.custom_identifier = 'lower register mapping #2'
    assert mapping.custom_identifier == 'lower register mapping #2'
