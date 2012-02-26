from abjad import *
import py.test


def test_MarkupCommand___init___01():
    '''`command` must be a non-empty string without spaces.'''
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('')")
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand(3.14159)")
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('one two')")
