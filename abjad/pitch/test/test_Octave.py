import pytest
from abjad.pitch import (
    NamedPitch,
    NamedPitchClass,
    Octave,
    NumberedPitch,
    NumberedPitchClass,
)


values = [
    ("'", 4),
    ("''", 5),
    ("'''", 6),
    ("''''", 7),
    ("bf,", 2),
    ("c'", 4),
    ("cs'", 4),
    ("gff''", 5),
    ('', 3),
    (',', 2),
    (',,', 1),
    (',,,', 0),
    ('-0', 0),
    ('-1', -1),
    ('-2', -2),
    ('-3', -3),
    ('-4', -4),
    ('0', 0),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('dss,,', 1),
    ('fake', ValueError),
    (('bf', 2), 2),
    (('c', 4), 4),
    (('cs', 4), 4),
    (('dss', 1), 1),
    (('gff', 5), 5),
    (-1, -1),
    (-2, -2),
    (-3, -3),
    (-4, -4),
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (NamedPitch("bs'"), 4),
    (NamedPitch('c'), 3),
    (NamedPitch('cf,'), 2),
    (NamedPitch(), 4),
    (NamedPitchClass("cs'"), 4),
    (NamedPitchClass('c'), 4),
    (NamedPitchClass('cf,'), 4),
    (None, 4),
    (NumberedPitch("bs'"), 5),
    (NumberedPitch('c'), 3),
    (NumberedPitch('cf,'), 1),
    (NumberedPitch(), 4),
    (NumberedPitchClass("bs'"), 4),
    (NumberedPitchClass('c'), 4),
    (NumberedPitchClass('cf,'), 4),
    (Octave(), 4),
    (Octave(3), 3),
    (Octave(5), 5),
    ]


@pytest.mark.parametrize('input_, expected_number', values)
def test_init(input_, expected_number):
    if (
        isinstance(expected_number, type) and
        issubclass(expected_number, Exception)
    ):
        with pytest.raises(expected_number):
            Octave(input_)
        return
    octave = Octave(input_)
    assert octave.number == expected_number
