# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_ChordQuality___eq___01():

    chord_quality = tonalanalysistools.ChordQuality('major')
    u = tonalanalysistools.ChordQuality('major')
    voice = tonalanalysistools.ChordQuality('minor')

    assert     chord_quality == chord_quality
    assert     chord_quality == u
    assert not chord_quality == voice

    assert     u == chord_quality
    assert     u == u
    assert not u == voice

    assert not voice == chord_quality
    assert not voice == u
    assert     voice == voice
