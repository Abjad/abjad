# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Skip___eq___01():

    skip_1 = scoretools.Skip((1, 4))
    skip_2 = scoretools.Skip((1, 4))
    skip_3 = scoretools.Skip((1, 8))

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3
