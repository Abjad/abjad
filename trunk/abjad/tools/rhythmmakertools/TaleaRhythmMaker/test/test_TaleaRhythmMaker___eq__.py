from abjad.tools import *


def test_TaleaRhythmMaker___eq___01():

    maker_1 = rhythmmakertools.TaleaRhythmMaker([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    maker_2 = rhythmmakertools.TaleaRhythmMaker([-1, 2, -3, 4], 16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert maker_1 == maker_1
    assert maker_1 == maker_2
    assert not maker_1 == 'foo'
    assert maker_2 == maker_1
    assert maker_2 == maker_2
    assert not maker_2 == 'foo'
    assert not 'foo' == maker_1
    assert not 'foo' == maker_2
    assert 'foo' == 'foo'
