# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import layouttools


def test_layouttools_SpacingIndication___eq___01():
    r'''Spacing indications compare equal when
    normalized spacing durations compare equal.
    '''

    tempo_indication = TempoMark(Duration(1, 8), 38)
    spacing_indication_1 = layouttools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    tempo_indication = TempoMark(Duration(1, 4), 76)
    spacing_indication_2 = layouttools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    assert spacing_indication_1 == spacing_indication_2


def test_layouttools_SpacingIndication___eq___02():
    r'''Spacing indications compare not equal when
    normalized spacing durations compare not equal.
    '''

    tempo_indication = TempoMark(Duration(1, 8), 38)
    spacing_indication_1 = layouttools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    tempo_indication = TempoMark(Duration(1, 8), 38)
    spacing_indication_2 = layouttools.SpacingIndication(
        tempo_indication, Duration(1, 78))

    assert spacing_indication_1 != spacing_indication_2
