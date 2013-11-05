# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_Staff___setattr___01():
    r'''Slots constrain staff attributes.
    '''

    staff = Staff([])

    assert py.test.raises(AttributeError, "staff.foo = 'bar'")
