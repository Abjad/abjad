import abjad


def test_Meter___iter___01():
    bh = abjad.Meter(abjad.TimeSignature((3, 8)))

    result = [x for x in bh]

    assert result == [
        ((0, 8), (1, 8)),
        ((1, 8), (2, 8)),
        ((2, 8), (3, 8)),
        ((0, 8), (3, 8)),
    ]
