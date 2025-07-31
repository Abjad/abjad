import pytest

import abjad

values: list[tuple] = []
values.extend((x / 2, (x / 2) % 12) for x in range(-48, 49))
values.extend(
    [
        ("bf,", 10),
        ("c'", 0),
        ("cs'", 1),
        ("gff''", 5),
        ("", 0),
        ("dss,,", 4),
        ("fake", ValueError),
        (("bf", 2), 10),
        (("c", 4), 0),
        (("cs", 4), 1),
        (("dss", 1), 4),
        (("gff", 5), 5),
        (abjad.NamedPitch("bs'"), 0),
        (abjad.NamedPitch("c"), 0),
        (abjad.NamedPitch("cf,"), 11),
        (abjad.NamedPitch(), 0),
        (abjad.NamedPitchClass("cs'"), 1),
        (abjad.NamedPitchClass("c"), 0),
        (abjad.NamedPitchClass("cf,"), 11),
        (None, 0),
        (abjad.NumberedPitch("bs'"), 0),
        (abjad.NumberedPitch("c"), 0),
        (abjad.NumberedPitch("cf,"), 11),
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
            abjad.NumberedPitchClass(input_)
        return
    instance = abjad.NumberedPitchClass(input_)
    assert float(instance) == expected_semitones
