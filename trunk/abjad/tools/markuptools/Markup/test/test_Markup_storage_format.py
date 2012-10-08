from abjad import *


def test_Markup_storage_format_01():

    markup = markuptools.Markup(r'\bold { foo }')

    assert repr(markup) == "Markup((MarkupCommand('bold', ['foo']),))"

    r'''
    markuptools.Markup((
        markuptools.MarkupCommand(
            'bold',
            [
                'foo'
            ]
            ),
        ))
    '''

    assert markup.storage_format == "markuptools.Markup((\n\tmarkuptools.MarkupCommand(\n\t\t'bold',\n\t\t[\n\t\t\t'foo'\n\t\t]\n\t\t),\n\t))"


def test_Markup_storage_format_02():

    markup = markuptools.Markup(r'\bold { allegro ma non troppo }', markup_name='non troppo')

    assert repr(markup) == "Markup((MarkupCommand('bold', ['allegro', 'ma', 'non', 'troppo']),), markup_name='non troppo')"

    r'''
    markuptools.Markup((
        markuptools.MarkupCommand(
            'bold',
            [
                'allegro',
                'ma',
                'non',
                'troppo'
            ]
            ),
        ),
        markup_name='non troppo'
        )
    '''

    assert markup.storage_format == "markuptools.Markup((\n\tmarkuptools.MarkupCommand(\n\t\t'bold',\n\t\t[\n\t\t\t'allegro',\n\t\t\t'ma',\n\t\t\t'non',\n\t\t\t'troppo'\n\t\t]\n\t\t),\n\t),\n\tmarkup_name='non troppo'\n\t)"
