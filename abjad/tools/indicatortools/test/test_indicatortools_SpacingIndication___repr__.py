# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.indicatortools import SpacingIndication
from abjad.tools.indicatortools import Tempo


def test_indicatortools_SpacingIndication___repr___01():
    r'''Repr is evaluable.
    '''

    indication_1 = SpacingIndication(Tempo(Duration(1, 8), 44), Duration(1, 68))
    indication_2 = SpacingIndication(indication_1)

    assert indication_1 is not indication_2
    assert indication_1 == indication_2
