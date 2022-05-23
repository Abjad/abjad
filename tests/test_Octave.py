import pytest

import abjad

values = [
    (-1, -1),
    (-2, -2),
    (-3, -3),
    (-4, -4),
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (abjad.Octave(), 4),
    (abjad.Octave(3), 3),
    (abjad.Octave(5), 5),
]


@pytest.mark.parametrize("input_, expected_number", values)
def test_init(input_, expected_number):
    if isinstance(expected_number, type) and issubclass(expected_number, Exception):
        with pytest.raises(expected_number):
            abjad.Octave(input_)
        return
    octave = abjad.Octave(input_)
    assert octave.number == expected_number


values = [
    ("'", 4),
    ("''", 5),
    ("'''", 6),
    ("''''", 7),
    ("", 3),
    (",", 2),
    (",,", 1),
    (",,,", 0),
]


@pytest.mark.parametrize("input_, expected_number", values)
def test_from_ticks(input_, expected_number):
    if isinstance(expected_number, type) and issubclass(expected_number, Exception):
        with pytest.raises(expected_number):
            abjad.Octave.from_ticks(input_)
        return
    octave = abjad.Octave.from_ticks(input_)
    assert octave.number == expected_number


values = [
    ("bf,", 2),
    ("c'", 4),
    ("cs'", 4),
    ("gff''", 5),
    ("dss,,", 1),
    (("bf", 2), 2),
    (("c", 4), 4),
    (("cs", 4), 4),
    (("dss", 1), 1),
    (("gff", 5), 5),
    (abjad.NamedPitch("bs'"), 4),
    (abjad.NamedPitch("c"), 3),
    (abjad.NamedPitch("cf,"), 2),
    (abjad.NamedPitch(), 4),
    (abjad.NamedPitchClass("cs'"), 4),
    (abjad.NamedPitchClass("c"), 4),
    (abjad.NamedPitchClass("cf,"), 4),
    (abjad.NumberedPitch("bs'"), 5),
    (abjad.NumberedPitch("c"), 3),
    (abjad.NumberedPitch("cf,"), 1),
    (abjad.NumberedPitch(), 4),
    (abjad.NumberedPitchClass("bs'"), 4),
    (abjad.NumberedPitchClass("c"), 4),
    (abjad.NumberedPitchClass("cf,"), 4),
]


@pytest.mark.parametrize("input_, expected_number", values)
def test_init_from_pitch(input_, expected_number):
    octave = abjad.NamedPitch(input_).octave
    assert octave.number == expected_number
