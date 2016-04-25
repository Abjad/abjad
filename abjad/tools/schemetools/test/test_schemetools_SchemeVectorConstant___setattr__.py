# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_schemetools_SchemeVectorConstant___setattr___01():
    r'''Scheme vector constants are immutable.
    '''

    scheme_vector_constant = schemetools.SchemeVectorConstant(True, True, False)
    assert pytest.raises(AttributeError, "scheme_vector_constant.foo = 'bar'")
