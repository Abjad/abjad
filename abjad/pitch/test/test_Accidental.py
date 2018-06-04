import pytest
from abjad.pitch import Accidental


values = [
    ("bf,", -1),
    ("c'", 0),
    ("cs'", 1),
    ("gff''", -2),
    ('####', 4.0),
    ('###', 3.0),
    ('###+', 3.5),
    ('##', 2.0),
    ('##+', 2.5),
    ('#', 1.0),
    ('#+', 1.5),
    ('', 0.0),
    ('+', 0.5),
    ('b', -1.0),
    ('bb', -2.0),
    ('bbb', -3.0),
    ('bbbb', -4.0),
    ('bbb~', -3.5),
    ('bb~', -2.5),
    ('b~', -1.5),
    ('dss,,', 2),
    ('f', -1.0),
    ('ff', -2.0),
    ('fff', -3.0),
    ('ffff', -4.0),
    ('fffqf', -3.5),
    ('ffqf', -2.5),
    ('fqf', -1.5),
    ('qf', -0.5),
    ('qs', 0.5),
    ('s', 1.0),
    ('sqs', 1.5),
    ('ss', 2.0),
    ('ssqs', 2.5),
    ('sss', 3.0),
    ('sssqs', 3.5),
    ('ssss', 4.0),
    ('tqf', -1.5),
    ('tqs', 1.5),
    ('~', -0.5),
    (('bf', 2), -1),
    (('c', 4), 0),
    (('cs', 4), 1),
    (('dss', 1), 2),
    (('gff', 5), -2),
    (-0, -0.0),
    (-0.0, 0.0),
    (-0.5, -0.5),
    (-1, -1.0),
    (-1.0, -1.0),
    (-1.5, -1.5),
    (-2, -2.0),
    (-2.0, -2.0),
    (-2.5, -2.5),
    (-3, -3.0),
    (-3.0, -3.0),
    (0, 0.0),
    (0.0, 0.0),
    (0.5, 0.5),
    (1, 1.0),
    (1.0, 1.0),
    (1.5, 1.5),
    (2, 2.0),
    (2.0, 2.0),
    (2.5, 2.5),
    (3, 3.0),
    (3.0, 3.0),
    (None, 0.0),
    ]


@pytest.mark.parametrize('input_, expected_semitones', values)
def test(input_, expected_semitones):
    if (
        isinstance(expected_semitones, type) and
        issubclass(expected_semitones, Exception)
    ):
        with pytest.raises(expected_semitones):
            Accidental(input_)
    else:
        accidental = Accidental(input_)
        assert accidental.semitones == expected_semitones
