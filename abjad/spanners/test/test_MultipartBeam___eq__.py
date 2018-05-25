import abjad


def test_MultipartBeam___eq___01():
    """
    Spanner is strict comparator.
    """

    spanner_1 = abjad.MultipartBeam()
    spanner_2 = abjad.MultipartBeam()

    assert not spanner_1 == spanner_2
