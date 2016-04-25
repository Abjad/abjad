# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_Markup___repr___01():

    markup = markuptools.Markup('foo bar')
    assert repr(markup) == "Markup(contents=('foo bar',))"


def test_markuptools_Markup___repr___02():

    markup = markuptools.Markup('foo bar', direction=Up)
    assert repr(markup) == "Markup(contents=('foo bar',), direction=Up)"


def test_markuptools_Markup___repr___03():

    markup = markuptools.Markup(contents=('foo', 'bar'), direction=Up)
    assert repr(markup) == "Markup(contents=('foo', 'bar'), direction=Up)"
