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
    '''Init markup with scheme style string.
    '''

    markup = markuptools.Markup("(markup #:draw-line '(0 . -1))", style_string='scheme')
    assert markup.format == "#(markup #:draw-line '(0 . -1))"


def test_Markup___init___05():
    '''Preserve all keywords when initializing from other markup instance.
    '''

    markup_1 = markuptools.Markup(
        'foo contents string', direction='up', markup_name='foo', style_string='backslash')
    markup_2 = markuptools.Markup(markup_1)

    assert markup_1 is not markup_2
    assert markup_1 == markup_2
    assert repr(markup_1) == repr(markup_2)
    assert markup_1._storage_format == markup_2._storage_format


def test_Markup___init___06():
    '''Preserve keywords when initializing from other markup instance
    but also overwrite keywords specified anew.
    '''

    markup_1 = markuptools.Markup(
        'foo contents string', direction='up', markup_name='foo', style_string='backslash')
    markup_2 = markuptools.Markup(markup_1, direction='down')

    assert markup_1 is not markup_2
    assert markup_2.contents_string == 'foo contents string'
    assert markup_2.direction == '_'
    assert markup_2.markup_name == 'foo'
    assert markup_2.style_string == 'backslash'
