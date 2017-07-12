# -*- coding: utf-8 -*-
import abjad
import pytest


def test_schemetools_SchemeColor___setattr___01():
    r'''Scheme colors are immutable.
    '''

    scheme_color = abjad.SchemeColor('ForestGreen')
    assert pytest.raises(AttributeError, "scheme_color.foo = 'bar'")
