import pytest

import abjad

values: list[tuple] = []
values.extend((x / 2, x / 2) for x in range(-48, 49))
values.extend(
    [
        ("bf,", -14),
        ("c'", 0),
        ("cs'", 1),
        ("gff''", 17),
        ("", 0),
        ("dss,,", -32),
        ("fake", ValueError),
        (("bf", 2), -14),
        (("c", 4), 0),
        (("cs", 4), 1),
        (("dss", 1), -32),
        (("gff", 5), 17),
        (abjad.NamedPitch("bs'"), 12),
        (abjad.NamedPitch("c"), -12),
        (abjad.NamedPitch("cf,"), -25),
        (abjad.NamedPitch(), 0),
        (abjad.NamedPitchClass("cs'"), 1),
        (abjad.NamedPitchClass("c"), 0),
        (abjad.NamedPitchClass("cf,"), 11),
        (None, 0),
        (abjad.NumberedPitch("bs'"), 12),
        (abjad.NumberedPitch("c"), -12),
        (abjad.NumberedPitch("cf,"), -25),
        (abjad.NumberedPitch(), 0),
        (abjad.NumberedPitchClass("bs'"), 0),
        (abjad.NumberedPitchClass("c"), 0),
        (abjad.NumberedPitchClass("cf,"), 11),
    ]
)


@pytest.mark.parametrize("input_, expected_semitones", values)
def test_init(input_, expected_semitones):
    if isinstance(expected_semitones, type) and issubclass(
        expected_semitones, Exception
    ):
        with pytest.raises(expected_semitones):
            abjad.NumberedPitch(input_)
        return
    instance = abjad.NumberedPitch(input_)
    assert float(instance) == expected_semitones
