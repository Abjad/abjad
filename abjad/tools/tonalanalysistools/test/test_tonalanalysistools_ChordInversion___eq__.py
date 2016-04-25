# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordInversion___eq___01():

    chord_inversion = tonalanalysistools.ChordInversion(0)
    u = tonalanalysistools.ChordInversion(0)
    voice = tonalanalysistools.ChordInversion(1)

    assert      chord_inversion == chord_inversion
    assert      chord_inversion == u
    assert not chord_inversion == voice

    assert      u == chord_inversion
    assert      u == u
    assert not u == voice

    assert not voice == chord_inversion
    assert not voice == u
    assert      voice == voice
