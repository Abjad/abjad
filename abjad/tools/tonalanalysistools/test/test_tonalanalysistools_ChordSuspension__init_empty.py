# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_ChordSuspension__init_empty_01():

    chord_suspension = tonalanalysistools.ChordSuspension()

    assert chord_suspension.start is None
    assert chord_suspension.stop is None
