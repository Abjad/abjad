from specificationtools.Division import Division
from specificationtools.DivisionList import DivisionList


def test_DivisionList___repr___01():

    divisions = []
    divisions.append(Division((2, 8), is_left_open=True))
    divisions.append(Division((5, 8)))
    divisions.append(Division((1, 8), is_right_open=True))
    division_list = DivisionList(divisions) 
    
    assert repr(division_list) == \
        'DivisionList([D((2, 8), D(5, 8), D(1, 8))], is_left_open=True, is_right_open=True)'
