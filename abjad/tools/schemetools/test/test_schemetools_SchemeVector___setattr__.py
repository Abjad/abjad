# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_schemetools_SchemeVector___setattr___01():
    r'''Scheme vectors are immutable.
    '''

    scheme_vector = schemetools.SchemeVector(True, True, False)
    assert pytest.raises(AttributeError, "scheme_vector.foo = 'bar'")
