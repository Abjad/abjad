from abjad import *


def test_Spanner___contains___01():

    class MockSpanner(spannertools.Spanner):
        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)
        def _copy_keyword_args(self, new):
            pass

    note = Note("c'4")

    spanner = MockSpanner([Note("c'4")])

    assert not note in spanner
