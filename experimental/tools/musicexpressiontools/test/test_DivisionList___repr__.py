# -*- encoding: utf-8 -*-
from experimental.tools.musicexpressiontools.Division import Division
from experimental.tools.musicexpressiontools.DivisionList import DivisionList


def test_DivisionList___repr___01():

    divisions = []
    divisions.append(Division((2, 8)))
    divisions.append(Division((5, 8)))
    divisions.append(Division((1, 8)))
    division_list = DivisionList(divisions)

    assert repr(division_list) == "DivisionList('[2, 8), [5, 8), [1, 8)')"