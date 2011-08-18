from abjad import *


def test_MarkupCommand___eq___01():

    a = markuptools.MarkupCommand('box', None, None)
    b = markuptools.MarkupCommand('box', ['hello'], None)
    c = markuptools.MarkupCommand('box', None, ['hello'])
    d = markuptools.MarkupCommand('box', ['hello'], ['hello'])
    e = markuptools.MarkupCommand('sox', None, None)

    assert a != b != c != d != e

def test_MarkupCommand___eq___02():

    a = markuptools.MarkupCommand('box', None, None)
    b = markuptools.MarkupCommand('box', None, None)

    assert a == b
