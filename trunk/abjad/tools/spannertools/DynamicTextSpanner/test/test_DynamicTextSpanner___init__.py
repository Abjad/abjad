from abjad import *


def test_DynamicTextSpanner___init___01():
    r'''Init empty dynamic text spanner.
    '''

    spanner = spannertools.DynamicTextSpanner()
    assert isinstance(spanner, spannertools.DynamicTextSpanner)
