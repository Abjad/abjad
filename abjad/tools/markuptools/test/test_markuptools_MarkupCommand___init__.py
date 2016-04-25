# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_markuptools_MarkupCommand___init___01():
    '''Command must be a nonempty string without spaces.
    '''

    assert pytest.raises(Exception, "markuptools.MarkupCommand('')")
    assert pytest.raises(Exception, "markuptools.MarkupCommand(3.14159)")
    assert pytest.raises(Exception, "markuptools.MarkupCommand('one two')")
