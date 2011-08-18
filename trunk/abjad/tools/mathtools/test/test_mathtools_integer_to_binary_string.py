from abjad import *
from abjad.tools import mathtools
import py.test


def test_mathtools_integer_to_binary_string_01():
    '''Return base-2 representation of integer n as string.'''

    assert mathtools.integer_to_binary_string(1) == '1'
    assert mathtools.integer_to_binary_string(2) == '10'
    assert mathtools.integer_to_binary_string(3) == '11'
    assert mathtools.integer_to_binary_string(4) == '100'
    assert mathtools.integer_to_binary_string(5) == '101'
    assert mathtools.integer_to_binary_string(6) == '110'
    assert mathtools.integer_to_binary_string(7) == '111'
    assert mathtools.integer_to_binary_string(8) == '1000'


def test_mathtools_integer_to_binary_string_02():

    assert mathtools.integer_to_binary_string(0) == '0'
    assert mathtools.integer_to_binary_string(-1) == '-1'
    assert mathtools.integer_to_binary_string(-2) == '-10'
    assert mathtools.integer_to_binary_string(-3) == '-11'


def test_mathtools_integer_to_binary_string_03():
    '''Raise TypeError for noninteger input.'''

    assert py.test.raises(TypeError, 'mathtools.integer_to_binary_string(5.5)')
