import abjad


def test_metertools_Meter___iter___01():

    bh = abjad.Meter(abjad.TimeSignature((3, 8)))

    result = [x for x in bh]

    assert result == [
        (abjad.Offset(0, 1), abjad.Offset(1, 8)),
        (abjad.Offset(1, 8), abjad.Offset(1, 4)),
        (abjad.Offset(1, 4), abjad.Offset(3, 8)),
        (abjad.Offset(0, 1), abjad.Offset(3, 8))
    ]
