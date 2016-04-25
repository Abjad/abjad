# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_SpacingIndication_normalized_spacing_duration_01():
    r'''LilyPond proportionalNotationDuration setting required
    for this spacing indication at quarter equals 60.
    '''

    tempo_indication = Tempo(Duration(1, 4), 120)
    spacing_indication = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 16)
        )
    assert spacing_indication.normalized_spacing_duration == Duration(1, 32)


def test_indicatortools_SpacingIndication_normalized_spacing_duration_02():
    r'''LilyPond proportionalNotationDuration setting required
    for this spacing indication at quarter equals 60
    is the same as the proportional notation duration set
    on this spacing indication when tempo indication set
    on this spacing indication is already quarter equals 60.
    '''

    tempo_indication = Tempo(Duration(1, 4), 60)
    spacing_indication = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 68)
        )
    assert spacing_indication.normalized_spacing_duration == Duration(1, 68)
