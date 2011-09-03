from abjad import *
from abjad.tools import mathtools


def test_mathtools_get_shared_numeric_sign_01():

    assert mathtools.get_shared_numeric_sign([1, 2, 3]) == 1
    assert mathtools.get_shared_numeric_sign([-1, -2, -3]) == -1
    assert mathtools.get_shared_numeric_sign([]) == 0
    assert mathtools.get_shared_numeric_sign([1, 2, -3]) is None
