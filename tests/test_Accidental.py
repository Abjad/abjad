import pytest
from abjad.pitch import Accidental


values = [
    ("bf,", -1, 'f'),
    ("c'", 0, ''),
    ("cs'", 1, 's'),
    ("gff''", -2, 'ff'),
    ('####', 4.0, 'ssss'),
    ('###', 3.0, 'sss'),
    ('###+', 3.5, 'sssqs'),
    ('##', 2.0, 'ss'),
    ('##+', 2.5, 'ssqs'),
    ('#', 1.0, 's'),
    ('#+', 1.5, 'tqs'),
    ('', 0.0, ''),
    ('+', 0.5, 'qs'),
    ('b', -1.0, 'f'),
    ('bb', -2.0, 'ff'),
    ('bbb', -3.0, 'fff'),
    ('bbbb', -4.0, 'ffff'),
    ('bbb~', -3.5, 'fffqf'),
    ('bb~', -2.5, 'ffqf'),
    ('b~', -1.5, 'tqf'),
    ('dss,,', 2, 'ss'),
    ('f', -1.0, 'f'),
    ('ff', -2.0, 'ff'),
    ('fff', -3.0, 'fff'),
    ('ffff', -4.0, 'ffff'),
    ('fffqf', -3.5, 'fffqf'),
    ('ffqf', -2.5, 'ffqf'),
    ('fqf', -1.5, 'tqf'),
    ('qf', -0.5, 'qf'),
    ('qs', 0.5, 'qs'),
    ('s', 1.0, 's'),
    ('sqs', 1.5, 'tqs'),
    ('ss', 2.0, 'ss'),
    ('ssqs', 2.5, 'ssqs'),
    ('sss', 3.0, 'sss'),
    ('sssqs', 3.5, 'sssqs'),
    ('ssss', 4.0, 'ssss'),
    ('tqf', -1.5, 'tqf'),
    ('tqs', 1.5, 'tqs'),
    ('~', -0.5, 'qf'),
    (('bf', 2), -1, 'f'),
    (('c', 4), 0, ''),
    (('cs', 4), 1, 's'),
    (('dss', 1), 2, 'ss'),
    (('gff', 5), -2, 'ff'),
    (-0, -0.0, ''),
    (-0.0, 0.0, ''),
    (-0.5, -0.5, 'qf'),
    (-1, -1.0, 'f'),
    (-1.0, -1.0, 'f'),
    (-1.5, -1.5, 'tqf'),
    (-2, -2.0, 'ff'),
    (-2.0, -2.0, 'ff'),
    (-2.5, -2.5, 'ffqf'),
    (-3, -3.0, 'fff'),
    (-3.0, -3.0, 'fff'),
    (0, 0.0, ''),
    (0.0, 0.0, ''),
    (0.5, 0.5, 'qs'),
    (1, 1.0, 's'),
    (1.0, 1.0, 's'),
    (1.5, 1.5, 'tqs'),
    (2, 2.0, 'ss'),
    (2.0, 2.0, 'ss'),
    (2.5, 2.5, 'ssqs'),
    (3, 3.0, 'sss'),
    (3.0, 3.0, 'sss'),
    (None, 0.0, ''),
    ]


@pytest.mark.parametrize('input_, semitones, string', values)
def test_init(input_, semitones, string):
    if (
        isinstance(semitones, type) and
        issubclass(semitones, Exception)
    ):
        with pytest.raises(semitones):
            Accidental(input_)
        return
    accidental = Accidental(input_)
    assert accidental.semitones == semitones
    assert str(accidental) == string
