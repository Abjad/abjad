# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_Markup_markup_name_01():

    markup = markuptools.Markup(r'\bold { allegro ma non troppo }')
    assert markup.markup_name is None


def test_markuptools_Markup_markup_name_02():

    markup = markuptools.Markup(r'\bold { allegro ma non troppo }', markup_name='non troppo')
    assert markup.markup_name == 'non troppo'
