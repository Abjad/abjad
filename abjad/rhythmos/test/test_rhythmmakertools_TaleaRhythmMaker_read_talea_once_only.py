import abjad
import pytest
from abjad import rhythmos


def test_rhythmos_TaleaRhythmMaker_read_talea_once_only_01():

    maker = rhythmos.TaleaRhythmMaker(
        read_talea_once_only=True,
        talea=rhythmos.Talea(
            counts=[1, 2, 3, 4],
            denominator=16,
            ),
        )

    divisions = [(3, 8), (3, 8), (3, 8), (3, 8)]
    string = 'maker(divisions)'
    assert pytest.raises(Exception, string)
