# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_markuptools_MarkupCommand___init___01():
    '''`command` must be a non-empty string without spaces.
    '''

    assert pytest.raises(AssertionError, "markuptools.MarkupCommand('')")
    assert pytest.raises(AssertionError, "markuptools.MarkupCommand(3.14159)")
    assert pytest.raises(AssertionError, "markuptools.MarkupCommand('one two')")
