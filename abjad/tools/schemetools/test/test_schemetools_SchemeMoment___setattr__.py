# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_schemetools_SchemeMoment___setattr___01():
    r'''Scheme moments are immutable.
    '''

    scheme_moment = schemetools.SchemeMoment((1, 64))
    assert pytest.raises(AttributeError, "scheme_moment.foo = 'bar'")
