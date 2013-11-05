# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Staff___setattr___01():
    r'''Slots constrain staff attributes.
    '''

    staff = Staff([])

    assert pytest.raises(AttributeError, "staff.foo = 'bar'")
