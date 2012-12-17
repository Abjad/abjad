from experimental.tools.divisiontools.Division import Division


def test_Division___repr___01():

    assert repr(Division((4, 8))) == "Division('[4, 8]')"
    assert repr(Division((4, 8), is_left_open=True)) == "Division('(4, 8]')"
    assert repr(Division((4, 8), is_right_open=True)) == "Division('[4, 8)')"
