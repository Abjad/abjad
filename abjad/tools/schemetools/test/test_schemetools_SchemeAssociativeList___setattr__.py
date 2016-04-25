# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_schemetools_SchemeAssociativeList___setattr___01():
    r'''Scheme associative lists are immutable.
    '''

    scheme_alist = schemetools.SchemeAssociativeList(
        ('space', 2), ('padding', 0.5))
    assert pytest.raises(AttributeError, "scheme_alist.foo = 'bar'")
