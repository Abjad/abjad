# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_schemetools_SchemeMoment___setattr___01():
    r'''Scheme moments are immutable.
    '''

    scheme_moment = schemetools.SchemeMoment((1, 64))
    assert pytest.raises(AttributeError, "scheme_moment.foo = 'bar'")
