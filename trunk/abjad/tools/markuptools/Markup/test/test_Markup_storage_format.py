from abjad import *


def test_Markup_storage_format_01():

    markup = markuptools.Markup(r'\bold { foo }')

    assert repr(markup) == "Markup(('\\\\bold { foo }',))"

    r'''
    markuptools.Markup(
        ('\\bold { foo }',)
        )
    '''

    assert markup.storage_format == "markuptools.Markup(\n\t('\\\\bold { foo }',)\n\t)"


def test_Markup_storage_format_02():

    markup = markuptools.Markup(r'\bold { allegro ma non troppo }', markup_name='non troppo')

    r'''
    markuptools.Markup(
        ('\\bold { allegro ma non troppo }',),
        markup_name='non troppo'
        )
    '''

    assert markup.storage_format == "markuptools.Markup(\n\t('\\\\bold { allegro ma non troppo }',),\n\tmarkup_name='non troppo'\n\t)"
