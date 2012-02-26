from abjad import *


def test_MarkupCommand___eq___01():

    a = markuptools.MarkupCommand('box')
    b = markuptools.MarkupCommand('box', 'hello')
    c = markuptools.MarkupCommand('box', ['hello', 'hello'])
    d = markuptools.MarkupCommand('sox')

    assert a != b != c != d

def test_MarkupCommand___eq___02():

    a = markuptools.MarkupCommand('box')
    b = markuptools.MarkupCommand('box')

    assert a == b
