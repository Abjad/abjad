# -*- encoding: utf-8 -*-
from abjad import *


def test_markuptools_Markup___format___01():

    markup = markuptools.Markup(r'\bold { foo }')

    assert systemtools.TestManager.compare(
        format(markup, 'storage'),
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
        markup_name='non troppo',
        )

    assert systemtools.TestManager.compare(
        format(markup, 'storage'),
        r'''
        markuptools.Markup(
            contents=(
                markuptools.MarkupCommand(
                    'bold',
                    ['allegro', 'ma', 'non', 'troppo']
                    ),
                ),
            markup_name='non troppo',
            )
        '''
        )
