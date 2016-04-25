# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension___eq___01():

    chord_suspension = tonalanalysistools.ChordSuspension(4, 3)
    u = tonalanalysistools.ChordSuspension(4, 3)
    voice = tonalanalysistools.ChordSuspension(2, 1)

    assert      chord_suspension == chord_suspension
    assert      chord_suspension == u
    assert not chord_suspension == voice

    assert      u == chord_suspension
    assert      u == u
    assert not u == voice

    assert not voice == chord_suspension
    assert not voice == u
    assert      voice == voice
