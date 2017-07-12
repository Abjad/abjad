# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_is_empty_01():

    chord_suspension = tonalanalysistools.ChordSuspension()

    assert chord_suspension.is_empty
