# -*- encoding: utf-8 -*-
from experimental import *


def test_DivisionList___repr___01():

    divisions = []
    divisions.append(durationtools.Division((2, 8)))
    divisions.append(durationtools.Division((5, 8)))
    divisions.append(durationtools.Division((1, 8)))
    division_list = musicexpressiontools.DivisionList(divisions)

    assert repr(division_list) == "DivisionList('2/8, 5/8, 1/8')"