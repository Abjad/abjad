import pytest

from abjad.pitch import NamedPitch, NamedPitchClass, NumberedPitch, NumberedPitchClass

values = []
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
        (NamedPitch("bs'"), 12),
        (NamedPitch("c"), -12),
        (NamedPitch("cf,"), -25),
        (NamedPitch(), 0),
        (NamedPitchClass("cs'"), 1),
        (NamedPitchClass("c"), 0),
        (NamedPitchClass("cf,"), 11),
        (None, 0),
        (NumberedPitch("bs'"), 12),
        (NumberedPitch("c"), -12),
        (NumberedPitch("cf,"), -25),
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
            NumberedPitch(input_)
        return
    instance = NumberedPitch(input_)
    assert float(instance) == expected_semitones
