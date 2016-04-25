# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordExtent___eq___01():

    chord_extent = tonalanalysistools.ChordExtent(5)
    u = tonalanalysistools.ChordExtent(5)
    voice = tonalanalysistools.ChordExtent(7)

    assert      chord_extent == chord_extent
    assert      chord_extent == u
    assert not chord_extent == voice

    assert      u == chord_extent
    assert      u == u
    assert not u == voice

    assert not voice == chord_extent
    assert not voice == u
    assert      voice == voice
