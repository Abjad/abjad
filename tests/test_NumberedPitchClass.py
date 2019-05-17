import pytest
from abjad.pitch import (
    NumberedPitchClass,
    NamedPitch,
    NamedPitchClass,
    NumberedPitch,
)


values = []
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
        (NamedPitch("bs'"), 0),
        (NamedPitch("c"), 0),
        (NamedPitch("cf,"), 11),
        (NamedPitch(), 0),
        (NamedPitchClass("cs'"), 1),
        (NamedPitchClass("c"), 0),
        (NamedPitchClass("cf,"), 11),
        (None, 0),
        (NumberedPitch("bs'"), 0),
        (NumberedPitch("c"), 0),
        (NumberedPitch("cf,"), 11),
        (NumberedPitch(), 0),
        (NumberedPitchClass("bs'"), 0),
        (NumberedPitchClass("c"), 0),
        (NumberedPitchClass("cf,"), 11),
    ]
)


@pytest.mark.parametrize("input_, expected_semitones", values)
def test_init(input_, expected_semitones):
    if isinstance(expected_semitones, type) and issubclass(
        expected_semitones, Exception
    ):
        with pytest.raises(expected_semitones):
            NumberedPitchClass(input_)
        return
    instance = NumberedPitchClass(input_)
    assert float(instance) == expected_semitones
