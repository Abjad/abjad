# -*- encoding: utf-8 -*-
import copy
from experimental import *


def test_Division___copy___01():

    division = musicexpressiontools.Division(
        (3, 6), 
        is_left_open=True, 
        is_right_open=True,
        )
    new_division = copy.deepcopy(division)

    assert new_division == division
    assert not new_division is division
