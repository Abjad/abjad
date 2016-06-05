# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_Markup___format___01():

    markup = markuptools.Markup(r'\bold { foo }')

    assert format(markup, 'storage') == stringtools.normalize(
        r'''
        markuptools.Markup(
            contents=(
                markuptools.MarkupCommand(
                    'bold',
                    ['foo']
                    ),
                ),
            )
        '''
        )


def test_markuptools_Markup___format___02():

    markup = markuptools.Markup(
        r'\bold { allegro ma non troppo }',
        )

    assert format(markup, 'storage') == stringtools.normalize(
        r'''
        markuptools.Markup(
            contents=(
                markuptools.MarkupCommand(
                    'bold',
                    ['allegro', 'ma', 'non', 'troppo']
                    ),
                ),
            )
        '''
        )
