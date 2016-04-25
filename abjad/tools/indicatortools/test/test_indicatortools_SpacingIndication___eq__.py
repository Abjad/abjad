# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_SpacingIndication___eq___01():
    r'''Spacing indications compare equal when
    normalized spacing durations compare equal.
    '''

    tempo_indication = Tempo(Duration(1, 8), 38)
    spacing_indication_1 = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    tempo_indication = Tempo(Duration(1, 4), 76)
    spacing_indication_2 = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    assert spacing_indication_1 == spacing_indication_2


def test_indicatortools_SpacingIndication___eq___02():
    r'''Spacing indications compare not equal when
    normalized spacing durations compare not equal.
    '''

    tempo_indication = Tempo(Duration(1, 8), 38)
    spacing_indication_1 = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 68))

    tempo_indication = Tempo(Duration(1, 8), 38)
    spacing_indication_2 = indicatortools.SpacingIndication(
        tempo_indication, Duration(1, 78))

    assert spacing_indication_1 != spacing_indication_2
