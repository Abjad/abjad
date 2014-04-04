# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_make_blank_line_markup_01():

    markup = markuptools.make_blank_line_markup()

    assert systemtools.TestManager.compare(
        format(markup, 'lilypond'),
        r'''
        \markup {
            \fill-line
                {
                    " "
                }
            }
        ''',
        )