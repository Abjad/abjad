from experimental.tools.divisiontools.DivisionList import DivisionList


def test_DivisionList_predicates_01():

    division_list = DivisionList([(4, 8), (4, 8), (3, 8)])
    
    assert division_list.is_left_closed
    assert division_list.is_right_closed

    assert division_list.is_closed
    assert not division_list.is_open

    assert not division_list.is_left_open
    assert not division_list.is_right_open

    assert not division_list.is_half_open
    assert not division_list.is_half_closed


def test_DivisionList_predicates_02():

    division_list = DivisionList([(4, 8), (4, 8), (3, 8)])
    division_list[0].is_left_closed = False

    assert not division_list.is_left_closed
    assert division_list.is_right_closed

    assert not division_list.is_closed
    assert not division_list.is_open

    assert division_list.is_left_open
    assert not division_list.is_right_open

    assert division_list.is_half_open
    assert division_list.is_half_closed


def test_DivisionList_predicates_03():

    division_list = DivisionList([(4, 8), (4, 8), (3, 8)])
    division_list[-1].is_right_closed = False

    assert division_list.is_left_closed
    assert not division_list.is_right_closed

    assert not division_list.is_closed
    assert not division_list.is_open

    assert not division_list.is_left_open
    assert division_list.is_right_open

    assert division_list.is_half_open
    assert division_list.is_half_closed


def test_DivisionList_predicates_04():

    division_list = DivisionList([(4, 8)])
    division_list[0].is_left_open = True
    division_list[0].is_right_open = True

    assert not division_list.is_left_closed
    assert not division_list.is_right_closed

    assert not division_list.is_closed
    assert division_list.is_open

    assert division_list.is_left_open
    assert division_list.is_right_open

    assert not division_list.is_half_open
    assert not division_list.is_half_closed
