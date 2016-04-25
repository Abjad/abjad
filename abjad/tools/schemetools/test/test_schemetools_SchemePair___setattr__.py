# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_schemetools_SchemePair___setattr___01():
    r'''Scehem pairs are immutable.
    '''

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert pytest.raises(AttributeError, "scheme_pair.foo = 'bar'")
