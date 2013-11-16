# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_indicatortools_LilyPondComment___setattr___01():
    r'''Slots constrain comment attributes.
    '''

    comment = indicatortools.LilyPondComment('foo')

    assert pytest.raises(AttributeError, "comment.foo = 'bar'")
