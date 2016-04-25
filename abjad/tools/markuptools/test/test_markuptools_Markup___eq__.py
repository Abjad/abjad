# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_Markup___eq___01():
    r'''No keywords.
    '''

    markup_1 = markuptools.Markup('foo')
    markup_2 = markuptools.Markup('foo')
    markup_3 = markuptools.Markup('bar')

    assert markup_1 == markup_2
    assert markup_2 == markup_1

    assert not markup_1 == markup_3
    assert not markup_3 == markup_1

    assert not markup_2 == markup_3
    assert not markup_3 == markup_2


def test_markuptools_Markup___eq___02():
    r'''With keywords.
    '''

    markup_1 = markuptools.Markup('foo')
    markup_2 = markuptools.Markup('foo', direction=Up)

    assert not markup_1 == markup_2
    assert not markup_2 == markup_1
