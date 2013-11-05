# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_markuptools_MarkupCommand___setattr___01():

    a = markuptools.MarkupCommand('draw-circle', 1, 0.1, False)
    assert pytest.raises(AttributeError, "a.foo = 'bar'")
