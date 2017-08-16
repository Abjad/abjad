import abjad


def test_spannertools_MultipartBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.MultipartBeam()
    spanner_2 = abjad.MultipartBeam()

    assert not spanner_1 == spanner_2
