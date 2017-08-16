import abjad


def test_spannertools_Spanner___contains___01():

    class MockSpanner(abjad.Spanner):

        def __init__(self, components=None):
            abjad.Spanner.__init__(self, components)

    note = abjad.Note("c'4")

    spanner = MockSpanner()
    abjad.attach(spanner, abjad.Note("c'4"))

    assert note not in spanner
