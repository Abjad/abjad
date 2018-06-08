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
    ('-A1', -1),
    ('-A10', -17),
    ('-A11', -18),
    ('-A12', -20),
    ('-A13', -22),
    ('-A14', -24),
    ('-A2', -3),
    ('-A3', -5),
    ('-A4', -6),
    ('-A5', -8),
    ('-A6', -10),
    ('-A7', -12),
    ('-A8', -13),
    ('-A9', -15),
    ('-AA1', -2),
    ('-AA10', -18),
    ('-AA11', -19),
    ('-AA12', -21),
    ('-AA13', -23),
    ('-AA14', -25),
    ('-AA2', -4),
    ('-AA3', -6),
    ('-AA4', -7),
    ('-AA5', -9),
    ('-AA6', -11),
    ('-AA7', -13),
    ('-AA8', -14),
    ('-AA9', -16),
    ('-AAA1', -3),
    ('-AAA10', -19),
    ('-AAA11', -20),
    ('-AAA12', -22),
    ('-AAA13', -24),
    ('-AAA14', -26),
    ('-AAA2', -5),
    ('-AAA3', -7),
    ('-AAA4', -8),
    ('-AAA5', -10),
    ('-AAA6', -12),
    ('-AAA7', -14),
    ('-AAA8', -15),
    ('-AAA9', -17),
    ('-M10', -16),
    ('-M13', -21),
    ('-M2', -2),
    ('-M3', -4),
    ('-M6', -9),
    ('-M7', -11),
    ('-M9', -14),
    ('-P1', -0),
    ('-P11', -17),
    ('-P12', -19),
    ('-P15', -24),
    ('-P4', -5),
    ('-P5', -7),
    ('-P8', -12),
    ('-P8', -12),
    ('-d1', -1),
    ('-d10', -14),
    ('-d11', -16),
    ('-d12', -18),
    ('-d13', -19),
    ('-d14', -21),
    ('-d2', -0),
    ('-d3', -2),
    ('-d4', -4),
    ('-d5', -6),
    ('-d6', -7),
    ('-d7', -9),
    ('-d8', -11),
    ('-d9', -12),
    ('-dd1', -2),
    ('-dd10', -13),
    ('-dd11', -15),
    ('-dd12', -17),
    ('-dd13', -18),
    ('-dd14', -20),
    ('-dd2', 1),
    ('-dd3', -1),
    ('-dd4', -3),
    ('-dd5', -5),
    ('-dd6', -6),
    ('-dd7', -8),
    ('-dd8', -10),
    ('-dd9', -11),
    ('-ddd1', -3),
    ('-ddd10', -12),
    ('-ddd11', -14),
    ('-ddd12', -16),
    ('-ddd13', -17),
    ('-ddd14', -19),
    ('-ddd2', 2),
    ('-ddd3', 0),
    ('-ddd4', -2),
    ('-ddd5', -4),
    ('-ddd6', -5),
    ('-ddd7', -7),
    ('-ddd8', -9),
    ('-ddd9', -10),
    ('-m10', -15),
    ('-m13', -20),
    ('-m14', -22),
    ('-m2', -1),
    ('-m3', -3),
    ('-m6', -8),
    ('-m7', -10),
    ('-m9', -13),
    ('A1', 1),
    ('A10', 17),
    ('A11', 18),
    ('A12', 20),
    ('A13', 22),
    ('A14', 24),
    ('A2', 3),
    ('A3', 5),
    ('A4', 6),
    ('A5', 8),
    ('A6', 10),
    ('A7', 12),
    ('A8', 13),
    ('A9', 15),
    ('AA1', 2),
    ('AA10', 18),
    ('AA11', 19),
    ('AA12', 21),
    ('AA13', 23),
    ('AA14', 25),
    ('AA2', 4),
    ('AA3', 6),
    ('AA4', 7),
    ('AA5', 9),
    ('AA6', 11),
    ('AA7', 13),
    ('AA8', 14),
    ('AA9', 16),
    ('AAA1', 3),
    ('AAA10', 19),
    ('AAA11', 20),
    ('AAA12', 22),
    ('AAA13', 24),
    ('AAA14', 26),
    ('AAA2', 5),
    ('AAA3', 7),
    ('AAA4', 8),
    ('AAA5', 10),
    ('AAA6', 12),
    ('AAA7', 14),
    ('AAA8', 15),
    ('AAA9', 17),
    ('M10', 16),
    ('M13', 21),
    ('M14', 23),
    ('M2', 2),
    ('M3', 4),
    ('M6', 9),
    ('M7', 11),
    ('M9', 14),
    ('P1', 0),
    ('P11', 17),
    ('P12', 19),
    ('P15', 24),
    ('P4', 5),
    ('P5', 7),
    ('P8', 12),
    ('d1', 1),
    ('d10', 14),
    ('d11', 16),
    ('d12', 18),
    ('d13', 19),
    ('d14', 21),
    ('d2', 0),
    ('d3', 2),
    ('d4', 4),
    ('d5', 6),
    ('d6', 7),
    ('d7', 9),
    ('d8', 11),
    ('d9', 12),
    ('dd1', 2),
    ('dd10', 13),
    ('dd11', 15),
    ('dd12', 17),
    ('dd13', 18),
    ('dd14', 20),
    ('dd2', -1),
    ('dd3', 1),
    ('dd4', 3),
    ('dd5', 5),
    ('dd6', 6),
    ('dd7', 8),
    ('dd8', 10),
    ('dd9', 11),
    ('ddd1', 3),
    ('ddd10', 12),
    ('ddd11', 14),
    ('ddd12', 16),
    ('ddd13', 17),
    ('ddd14', 19),
    ('ddd2', -2),
    ('ddd3', 0),
    ('ddd4', 2),
    ('ddd5', 4),
    ('ddd6', 5),
    ('ddd7', 7),
    ('ddd8', 9),
    ('ddd9', 10),
    ('m10', 15),
    ('m13', 20),
    ('m14', 22),
    ('m2', 1),
    ('m3', 3),
    ('m6', 8),
    ('m7', 10),
    ('m9', 13),
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
def test_init(input_, semitones):
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
