import abjad


def test_spannertools_Spanner___contains___01():

    class MockSpanner(abjad.Spanner):

        def __init__(self, leaves=None):
            abjad.Spanner.__init__(self, leaves)

    note = abjad.Note("c'4")

    spanner = MockSpanner()
    abjad.attach(spanner, abjad.select(abjad.Note("c'4")))

    assert note not in spanner
