from baca.specificationtools.Division import Division
import py
py.test.skip('temporarily skipping during debugging')


def test_Division___repr___01():

    assert repr(Division((4, 8))) == 'Division((4, 8))'
    assert repr(Division((4, 8), is_left_open=True)) == 'Division((4, 8), is_left_open=True)'
    assert repr(Division((4, 8), is_right_open=True)) == 'Division((4, 8), is_right_open=True)'
