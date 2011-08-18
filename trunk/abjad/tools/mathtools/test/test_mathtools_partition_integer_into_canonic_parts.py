from abjad import *
from abjad.tools import mathtools
import py.test


def test_mathtools_partition_integer_into_canonic_parts_01():

    assert mathtools.partition_integer_into_canonic_parts(1) == (1, )
    assert mathtools.partition_integer_into_canonic_parts(2) == (2, )
    assert mathtools.partition_integer_into_canonic_parts(3) == (3, )
    assert mathtools.partition_integer_into_canonic_parts(4) == (4, )
    assert mathtools.partition_integer_into_canonic_parts(5) == (4, 1)
    assert mathtools.partition_integer_into_canonic_parts(6) == (6, )
    assert mathtools.partition_integer_into_canonic_parts(7) == (7, )
    assert mathtools.partition_integer_into_canonic_parts(8) == (8, )
    assert mathtools.partition_integer_into_canonic_parts(9) == (8, 1)
    assert mathtools.partition_integer_into_canonic_parts(10) == (8, 2)


def test_mathtools_partition_integer_into_canonic_parts_02():

    assert mathtools.partition_integer_into_canonic_parts(11) == (8, 3)
    assert mathtools.partition_integer_into_canonic_parts(12) == (12, )
    assert mathtools.partition_integer_into_canonic_parts(13) == (12, 1)
    assert mathtools.partition_integer_into_canonic_parts(14) == (14, )
    assert mathtools.partition_integer_into_canonic_parts(15) == (15, )
    assert mathtools.partition_integer_into_canonic_parts(16) == (16, )
    assert mathtools.partition_integer_into_canonic_parts(17) == (16, 1)
    assert mathtools.partition_integer_into_canonic_parts(18) == (16, 2)
    assert mathtools.partition_integer_into_canonic_parts(19) == (16, 3)
    assert mathtools.partition_integer_into_canonic_parts(20) == (16, 4)


def test_mathtools_partition_integer_into_canonic_parts_03():

    assert mathtools.partition_integer_into_canonic_parts(-11) == (-8, -3)
    assert mathtools.partition_integer_into_canonic_parts(-12) == (-12, )
    assert mathtools.partition_integer_into_canonic_parts(-13) == (-12, -1)
    assert mathtools.partition_integer_into_canonic_parts(-14) == (-14, )
    assert mathtools.partition_integer_into_canonic_parts(-15) == (-15, )
    assert mathtools.partition_integer_into_canonic_parts(-16) == (-16, )
    assert mathtools.partition_integer_into_canonic_parts(-17) == (-16, -1)
    assert mathtools.partition_integer_into_canonic_parts(-18) == (-16, -2)
    assert mathtools.partition_integer_into_canonic_parts(-19) == (-16, -3)
    assert mathtools.partition_integer_into_canonic_parts(-20) == (-16, -4)


def test_mathtools_partition_integer_into_canonic_parts_04():

    assert mathtools.partition_integer_into_canonic_parts(
        11, direction = 'little-endian') == (3, 8)
    assert mathtools.partition_integer_into_canonic_parts(
        12, direction = 'little-endian') == (12, )
    assert mathtools.partition_integer_into_canonic_parts(
        13, direction = 'little-endian') == (1, 12)
    assert mathtools.partition_integer_into_canonic_parts(
        14, direction = 'little-endian') == (14, )
    assert mathtools.partition_integer_into_canonic_parts(
        15, direction = 'little-endian') == (15, )
    assert mathtools.partition_integer_into_canonic_parts(
        16, direction = 'little-endian') == (16, )
    assert mathtools.partition_integer_into_canonic_parts(
        17, direction = 'little-endian') == (1, 16)
    assert mathtools.partition_integer_into_canonic_parts(
        18, direction = 'little-endian') == (2, 16)
    assert mathtools.partition_integer_into_canonic_parts(
        19, direction = 'little-endian') == (3, 16)
    assert mathtools.partition_integer_into_canonic_parts(
        20, direction = 'little-endian') == (4, 16)


def test_mathtools_partition_integer_into_canonic_parts_05():

    assert py.test.raises(
        TypeError, 'mathtools.partition_integer_into_canonic_parts(7.5)')
