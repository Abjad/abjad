from abjad import *


def test_Markup___init___01():
    '''Init markup with string.
    '''

    markup = markuptools.Markup('foo')
    assert str(markup) == '\\markup { foo }'


def test_Markup___init___02():
    '''Init markup with other markup instance.
    '''

    markup_1 = markuptools.Markup('foo')
    markup_2 = markuptools.Markup(markup_1)

    assert str(markup_1) == '\\markup { foo }'
    assert str(markup_2) == '\\markup { foo }'


def test_Markup___init___03():
    '''Init markup with nonstring and nonmarkup instance.
    '''

    markup = markuptools.Markup(27)
    assert str(markup) == '\\markup { 27 }'



def test_Markup___init___04():
    '''Init markup from MarkupCommand.
    '''

    command = markuptools.MarkupCommand('flat')
    markup = markuptools.Markup(command)
    assert str(markup) == '\\markup { \\flat }'


def test_Markup___init___05():
    '''Init markup from sequence of strings or MarkupCommands.
    '''

    command_1 = markuptools.MarkupCommand('flat')
    command_2 = markuptools.MarkupCommand('sharp')
    markup = markuptools.Markup(['X', command_1, 'Y', command_2, 'Z'])
    assert str(markup) == '\\markup { X \\flat Y \\sharp Z }'


def test_Markup___init___06():
    '''Preserve all keywords when initializing from other markup instance.
    '''

    markup_1 = markuptools.Markup(
        'foo contents string', direction=Up, markup_name='foo')
    markup_2 = markuptools.Markup(markup_1)

    assert markup_1 is not markup_2
    assert markup_1 == markup_2
    assert repr(markup_1) == repr(markup_2)
    assert markup_1._storage_format == markup_2._storage_format


def test_Markup___init___07():
    '''Preserve keywords when initializing from other markup instance
    but also overwrite keywords specified anew.
    '''

    markup_1 = markuptools.Markup(
        'foo contents string', direction=Up, markup_name='foo')
    markup_2 = markuptools.Markup(markup_1, direction=Down)

    assert markup_1 is not markup_2
    assert markup_2.contents == ('foo contents string',)
    assert markup_2.direction is Down
    assert markup_2.markup_name == 'foo'
