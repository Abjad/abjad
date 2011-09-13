from abjad import *


def test_DynamicTextSpanner___init___01():
    '''Init empty dynamic text spanner.
    '''

    spanner = spannertools.DynamicTextSpanner()
    assert isinstance(spanner, spannertools.DynamicTextSpanner)
