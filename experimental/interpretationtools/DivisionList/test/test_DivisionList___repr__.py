from experimental.interpretationtools.Division import Division
from experimental.interpretationtools.DivisionList import DivisionList


def test_DivisionList___repr___01():

    divisions = []
    divisions.append(Division((2, 8), is_left_open=True))
    divisions.append(Division((5, 8)))
    divisions.append(Division((1, 8), is_right_open=True))
    division_list = DivisionList(divisions) 
    
    assert repr(division_list) == "DivisionList('(2, 8], [5, 8], [1, 8)')"
