# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_mathtools_remove_powers_of_two_01():
    r'''Remove powers of two from integer n.
    '''

    assert mathtools.remove_powers_of_two(10) == 5
    assert mathtools.remove_powers_of_two(20) == 5
    assert mathtools.remove_powers_of_two(30) == 15
    assert mathtools.remove_powers_of_two(40) == 5
    assert mathtools.remove_powers_of_two(50) == 25
    assert mathtools.remove_powers_of_two(60) == 15
    assert mathtools.remove_powers_of_two(70) == 35
    assert mathtools.remove_powers_of_two(80) == 5
    assert mathtools.remove_powers_of_two(90) == 45


def test_mathtools_remove_powers_of_two_02():
    r'''Raise TypeError on noninteger n.
    Raise ValueError on nonpositive n.
    '''

    assert pytest.raises(TypeError, "mathtools.remove_powers_of_two('foo')")
    assert pytest.raises(ValueError, 'mathtools.remove_powers_of_two(-1)')
