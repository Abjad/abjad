# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Staff___setattr___01():
    r'''Slots constrain staff attributes.
    '''

    staff = Staff([])

    assert pytest.raises(AttributeError, "staff.foo = 'bar'")
