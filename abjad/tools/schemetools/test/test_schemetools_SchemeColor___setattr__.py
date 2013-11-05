# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_schemetools_SchemeColor___setattr___01():
    r'''Scheme colors are immutable.
    '''

    scheme_color = schemetools.SchemeColor('ForestGreen')
    assert pytest.raises(AttributeError, "scheme_color.foo = 'bar'")
