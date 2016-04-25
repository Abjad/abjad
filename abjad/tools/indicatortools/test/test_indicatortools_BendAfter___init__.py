# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_BendAfter___init___01():
    r'''Initialize bend from bend amount.
    '''

    bend = indicatortools.BendAfter(16)
    assert isinstance(bend, indicatortools.BendAfter)


def test_indicatortools_BendAfter___init___02():
    r'''Initialize bend from other bend.
    '''

    bend_1 = indicatortools.BendAfter(16)
    bend_2 = indicatortools.BendAfter(bend_1)

    assert isinstance(bend_1, indicatortools.BendAfter)
    assert isinstance(bend_2, indicatortools.BendAfter)
    assert bend_1 == bend_2
    assert bend_1 is not bend_2
