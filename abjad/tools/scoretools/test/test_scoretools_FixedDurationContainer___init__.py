# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_FixedDurationContainer___init___01():
    r'''Initializes fixed-duration container from empty input.
    '''

    container = scoretools.FixedDurationContainer()

    assert container.target_duration == Duration(1, 4)
    assert not len(container)
