# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment___init___01():
    r'''Initializes vertical moment from empty input.
    '''

    vertical_moment = selectiontools.VerticalMoment()

    assert repr(vertical_moment) == 'VerticalMoment()'
