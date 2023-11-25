import collections

import abjad


def test_pcollections_sequence():
    """
    All pitch collections are registered as sequences.
    """

    for pcollection in (
        abjad.PitchClassSegment([0, 1, 2]),
        abjad.PitchClassSet([0, 1, 2]),
        abjad.PitchSegment([0, 1, 2]),
        abjad.PitchSet([0, 1, 2]),
        abjad.TwelveToneRow([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
    ):
        assert isinstance(pcollection, collections.abc.Sequence)
