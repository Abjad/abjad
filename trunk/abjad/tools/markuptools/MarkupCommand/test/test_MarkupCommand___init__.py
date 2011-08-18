from abjad import *
import py.test


def test_MarkupCommand___init___01():
    '''`command` must be a non-empty string without spaces.'''
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('', None, None)")
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand(3.14159, None, None)")
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('one two', None, None)")


def test_MarkupCommand___init___02():
    '''`args` must be None or a non-zero length list.'''
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('box', 3, None)")
    a = markuptools.MarkupCommand('box', None, None)
    b = markuptools.MarkupCommand('box', ['test'], None)


def test_MarkupCommand___init___03():
    '''`markup` must be None or a non-zero length list
        of strings and/or `MarkupCommand`s.'''
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('box', None, 3)")
    assert py.test.raises(AssertionError, "markuptools.MarkupCommand('box', None, [3])")
    markuptools.MarkupCommand('box', None, None)
    markuptools.MarkupCommand('box', None, ['test'])
    markuptools.MarkupCommand('box', None, [markuptools.MarkupCommand('box', None, None)])


def test_MarkupCommand___init___04():
    '''`is_braced` defaults to `True`.'''
    a = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    assert a.is_braced == True
