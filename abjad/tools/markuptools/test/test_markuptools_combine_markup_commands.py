# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_combine_markup_commands_01():

    markup_a = markuptools.MarkupCommand(
        'draw-circle', 4, 0.4, False)
    markup_b = markuptools.MarkupCommand(
        'filled-box',
        schemetools.SchemePair(-4, 4),
        schemetools.SchemePair(-0.5, 0.5),
        1,
        )
    markup_c = "some text"
    new_markup = markuptools.combine_markup_commands(
        markup_a, markup_b, markup_c)

    assert systemtools.TestManager.compare(
        format(new_markup, 'lilypond'),
        r'''
        \combine
            \combine
                \draw-circle
                    #4
                    #0.4
                    ##f
                \filled-box
                    #'(-4 . 4)
                    #'(-0.5 . 0.5)
                    #1
            "some text"
        ''',
        )


def test_markuptools_combine_markup_commands_02():

    markup_a = 'only a little text'
    assert markuptools.combine_markup_commands(markup_a) == markup_a
