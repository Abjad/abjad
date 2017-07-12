# -*- coding: utf-8 -*-
import abjad
import pytest


def test_schemetools_SchemeMoment___setattr___01():
    r'''Scheme moments are immutable.
    '''

    scheme_moment = abjad.SchemeMoment((1, 64))
    assert pytest.raises(AttributeError, "scheme_moment.foo = 'bar'")
