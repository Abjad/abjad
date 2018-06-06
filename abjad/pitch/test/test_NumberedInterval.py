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
    ('A1', 1),
    ('A2', 3),
    ('A3', 5),
    ('A4', 6),
    ('A5', 8),
    ('A6', 10),
    ('A7', 12),
    ('AA1', 2),
    ('AA2', 4),
    ('AA3', 6),
    ('AA4', 7),
    ('AA5', 9),
    ('AA6', 11),
    ('AA7', 13),
    ('AAA1', 3),
    ('AAA2', 5),
    ('AAA3', 7),
    ('AAA4', 8),
    ('AAA5', 10),
    ('AAA6', 12),
    ('AAA7', 14),
    ('M2', 2),
    ('M3', 4),
    ('M6', 9),
    ('M7', 11),
    ('P1', 0),
    ('P4', 5),
    ('P5', 7),
    ('P8', 12),
    ('d1', 1),
    ('d2', 0),
    ('d3', 2),
    ('d4', 4),
    ('d5', 6),
    ('d6', 7),
    ('d7', 9),
    ('dd1', 0),
    ('dd2', -1),
    ('dd3', 1),
    ('dd4', 3),
    ('dd5', 5),
    ('dd6', 6),
    ('dd7', 8),
    ('ddd1', -1),
    ('ddd2', -2),
    ('ddd3', 0),
    ('ddd4', 2),
    ('ddd5', 4),
    ('ddd6', 5),
    ('ddd7', 7),
    ('m2', 1),
    ('m3', 3),
    ('m6', 8),
    ('m7', 10),
    ('-A1', -1),
    ('-A2', -3),
    ('-A3', -5),
    ('-A4', -6),
    ('-A5', -8),
    ('-A6', -10),
    ('-A7', -12),
    ('-AA1', -2),
    ('-AA2', -4),
    ('-AA3', -6),
    ('-AA4', -7),
    ('-AA5', -9),
    ('-AA6', -11),
    ('-AA7', -13),
    ('-AAA1', -3),
    ('-AAA2', -5),
    ('-AAA3', -7),
    ('-AAA4', -8),
    ('-AAA5', -10),
    ('-AAA6', -12),
    ('-AAA7', -14),
    ('-M2', -2),
    ('-M3', -4),
    ('-M6', -9),
    ('-M7', -11),
    ('-P1', -0),
    ('-P4', -5),
    ('-P5', -7),
    ('-P8', -12),
    ('-d1', -1),
    ('-d1', -1),
    ('-d2', -0),
    ('-d3', -2),
    ('-d4', -4),
    ('-d5', -6),
    ('-d6', -7),
    ('-d7', -9),
    ('-dd1', 0),  # Is this correct?
    ('-dd2', 1),
    ('-dd3', -1),
    ('-dd4', -3),
    ('-dd5', -5),
    ('-dd6', -6),
    ('-dd7', -8),
    ('-ddd1', 1),
    ('-ddd2', 2),
    ('-ddd3', 0),
    ('-ddd4', -2),
    ('-ddd5', -4),
    ('-ddd6', -5),
    ('-ddd7', -7),
    ('-m2', -1),
    ('-m3', -3),
    ('-m6', -8),
    ('-m7', -10),
    ])

values.extend([
    (('M', 1), ValueError),
    (('M', 4), ValueError),
    (('M', 5), ValueError),
    (('P', 2), ValueError),
    (('P', 3), ValueError),
    (('P', 6), ValueError),
    (('P', 7), ValueError),
    (('m', 1), ValueError),
    (('m', 4), ValueError),
    (('m', 5), ValueError),
    ])


@pytest.mark.parametrize('input_, semitones', values)
def test_01(input_, semitones):
    class_ = NumberedInterval
    if (
        isinstance(semitones, type) and
        issubclass(semitones, Exception)
    ):
        with pytest.raises(semitones):
            class_(input_)
    else:
        instance = class_(input_)
        assert float(instance) == semitones
