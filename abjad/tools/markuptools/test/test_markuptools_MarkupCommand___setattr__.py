# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_markuptools_MarkupCommand___setattr___01():

    command = markuptools.MarkupCommand('draw-circle', 1, 0.1, False)
    assert pytest.raises(AttributeError, "command.foo = 'bar'")
