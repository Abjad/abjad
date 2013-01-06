from experimental.tools.settingtools.Division import Division


def test_Division_predicates_01():

    division = Division((4, 8))

    assert division.is_left_closed
    assert division.is_right_closed

    assert division.is_closed
    assert not division.is_open

    assert not division.is_left_open
    assert not division.is_right_open

    assert not division.is_half_open
    assert not division.is_half_closed


def test_Division_predicates_02():

    division = Division((4, 8), is_left_open=True)

    assert not division.is_left_closed
    assert division.is_right_closed

    assert not division.is_closed
    assert not division.is_open

    assert division.is_left_open
    assert not division.is_right_open

    assert division.is_half_open
    assert division.is_half_closed


def test_Division_predicates_03():

    division = Division((4, 8), is_right_open=True)

    assert division.is_left_closed
    assert not division.is_right_closed

    assert not division.is_closed
    assert not division.is_open

    assert not division.is_left_open
    assert division.is_right_open

    assert division.is_half_open
    assert division.is_half_closed


def test_Division_predicates_04():

    division = Division((4, 8), is_left_open=True, is_right_open=True)

    assert not division.is_left_closed
    assert not division.is_right_closed

    assert not division.is_closed
    assert division.is_open

    assert division.is_left_open
    assert division.is_right_open

    assert not division.is_half_open
    assert not division.is_half_closed
