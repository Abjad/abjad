from abjad import *


def test_Spanner___eq___01():
    '''Spanner is strict comparator.
    '''

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    spanner_1 = MockSpanner()
    spanner_2 = MockSpanner()

    assert not spanner_1 == spanner_2
