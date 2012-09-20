from experimental.divisiontools.Division import Division
import py
py.test.skip('deprecated')


def test_Division___eq___01():

    assert Division((4, 8)) == Division((4, 8))

    assert not Division((4, 8), is_left_open=True) == Division((4, 8))
    assert Division((4, 8), is_left_open=True) == Division((4, 8), is_left_open=True)

    assert not Division((4, 8), is_right_open=True) == Division((4, 8))
    assert Division((4, 8), is_right_open=True) == Division((4, 8), is_right_open=True)
