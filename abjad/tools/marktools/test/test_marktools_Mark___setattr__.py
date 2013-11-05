# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_marktools_Mark___setattr___01():
    r'''Slots constraint mark attributes.
    '''

    mark = marktools.Mark()

    assert pytest.raises(AttributeError, "mark.foo = 'bar'")
