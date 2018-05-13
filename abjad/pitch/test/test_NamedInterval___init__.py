import pytest
from abjad.pitch import (
    NamedInterval,
    NamedIntervalClass,
    NumberedInterval,
    NumberedIntervalClass,
)


values = []
values.extend((x, x) for x in range(-48, 49))
values.extend([
    ('d1', -1),
    ('P1', 0),
    ('A1', 1),
    ('d2', 0),
    ('m2', 1),
    ('M2', 2),
    ('A2', 3),
    ('d3', 2),
    ('m3', 3),
    ('M3', 4),
    ('A3', 5),
    ('d4', 4),
    ('P4', 5),
    ('A4', 6),
    ('d5', 6),
    ('P5', 7),
    ('A5', 8),
    ('d6', 7),
    ('m6', 8),
    ('M6', 9),
    ('A6', 10),
    ('d7', 9),
    ('m7', 10),
    ('M7', 11),
    ('A7', 12),
    ])


@pytest.mark.parametrize('input_, expected_semitones', values)
def test_01(input_, expected_semitones):
    class_ = NamedInterval
    if (
        isinstance(expected_semitones, type) and
        issubclass(expected_semitones, Exception)
    ):
        with pytest.raises(expected_semitones):
            class_(input_)
    else:
        instance = class_(input_)
        assert float(instance) == expected_semitones
