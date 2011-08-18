from abjad import *
import py.test


def test_MarkupCommand___setattr___01():

    a = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    assert py.test.raises(AttributeError, "a.foo = 'bar'")
