# -*- coding: utf-8 -*-
from abjad import *


def test_markuptools_Markup___init___01():
    r'''Initialize markup with string.
    '''

    markup = markuptools.Markup('foo')
    assert str(markup) == '\\markup { foo }'


def test_markuptools_Markup___init___02():
    r'''Initialize markup with other markup instance.
    '''

    markup_1 = markuptools.Markup('foo')
    markup_2 = markuptools.Markup(markup_1)

    assert str(markup_1) == '\\markup { foo }'
    assert str(markup_2) == '\\markup { foo }'


def test_markuptools_Markup___init___03():
    r'''Initialize markup with nonstring and nonmarkup instance.
    '''

    markup = markuptools.Markup(27)
    assert str(markup) == '\\markup { 27 }'



def test_markuptools_Markup___init___04():
    r'''Initialize markup from MarkupCommand.
    '''

    command = markuptools.MarkupCommand('flat')
    markup = markuptools.Markup(command)
    assert format(str(markup)) == stringtools.normalize(
        r'''
        \markup {
            \flat
            }
        ''',
        )


def test_markuptools_Markup___init___05():
    r'''Initialize markup from sequence of strings or MarkupCommands.
    '''

    command_1 = markuptools.MarkupCommand('flat')
    command_2 = markuptools.MarkupCommand('sharp')
    markup = markuptools.Markup(['X', command_1, 'Y', command_2, 'Z'])
    assert format(str(markup)) == stringtools.normalize(
        r'''
        \markup {
            X
            \flat
            Y
            \sharp
            Z
            }
        ''',
        )

def test_markuptools_Markup___init___06():
    r'''Preserve all keywords when initializing from other markup instance.
    '''

    markup_1 = markuptools.Markup('foo contents string', direction=Up)
    markup_2 = markuptools.Markup(markup_1)

    assert markup_1 is not markup_2
    assert markup_1 == markup_2
    assert repr(markup_1) == repr(markup_2)
    assert format(markup_1) == format(markup_2)


def test_markuptools_Markup___init___07():
    r'''Preserve keywords when initializing from other markup instance
    but also overwrite keywords specified anew.
    '''

    markup_1 = markuptools.Markup('foo contents string', direction=Up)
    markup_2 = markuptools.Markup(markup_1, direction=Down)

    assert markup_1 is not markup_2
    assert markup_2.contents == ('foo contents string',)
    assert markup_2.direction == Down


def test_markuptools_Markup___init___08():

    fraction_one = markuptools.Markup.fraction(3, 4)
    fraction_two = markuptools.Markup.fraction(9, 8)
    delimiter_string = ':'
    markup = markuptools.Markup([fraction_one, delimiter_string, fraction_two])
    markup = markup.pad_around(0.5).box()

    assert format(markup, 'lilypond') == stringtools.normalize(
        r'''
        \markup {
            \box
                \pad-around
                    #0.5
                    {
                        \fraction
                            3
                            4
                        :
                        \fraction
                            9
                            8
                    }
            }
        '''
        )
