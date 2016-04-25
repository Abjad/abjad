# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_greatest_common_divisor_01():
    r'''Greatest common integer divisor of integers.
    '''

    assert mathtools.greatest_common_divisor(84, -96, -144) == 12
    assert mathtools.greatest_common_divisor(84, 85) == 1
    assert mathtools.greatest_common_divisor(-84) == 84
    assert mathtools.greatest_common_divisor(6, 8, 12) == 2
    assert mathtools.greatest_common_divisor(-8, -12) == 4
    assert mathtools.greatest_common_divisor(11, 12) == 1


def test_mathtools_greatest_common_divisor_02():
    r'''Raise exception on noninteger input.
    '''

    assert pytest.raises(TypeError, "mathtools.greatest_common_divisor('foo')")
