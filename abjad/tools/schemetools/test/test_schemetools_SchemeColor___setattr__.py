# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_schemetools_SchemeColor___setattr___01():
    r'''Scheme colors are immutable.
    '''

    scheme_color = schemetools.SchemeColor('ForestGreen')
    assert pytest.raises(AttributeError, "scheme_color.foo = 'bar'")
