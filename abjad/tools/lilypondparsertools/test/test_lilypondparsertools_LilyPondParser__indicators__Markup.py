# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__Markup_01():

    target = Staff([Note(0, 1)])
    markup = markuptools.Markup('hello!', Up)
    attach(markup, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c'1 ^ \markup { hello! }
        }
        '''
        )

    string = r'''\new Staff { c'1 ^ "hello!" }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(inspect_(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_02():

    target = Staff([Note(0, (1, 4))])
    markup = markuptools.Markup(['X', 'Y', 'Z', 'a b c'], Down)
    attach(markup, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c'4
                _ \markup {
                    X
                    Y
                    Z
                    "a b c"
                    }
        }
        '''
        )

    string = r'''\new Staff { c' _ \markup { X Y Z "a b c" } }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(inspect_(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_03():
    r'''Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    '''

    target = Staff([Note(0, (1, 4)), Note(2, (1, 4))])
    markup = markuptools.Markup('hello', Up)
    attach(markup, target[0])
    articulation = Articulation('.')
    attach(articulation, target[0])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 -\staccato ^ \markup { hello }
            d'4
        }
        '''
        )

    string = r'''\new Staff { c' ^ \markup { hello } -. d' }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(inspect_(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_04():

    command1 = markuptools.MarkupCommand('bold', ['A', 'B', 'C'])
    command2 = markuptools.MarkupCommand('italic', '123')
    markup = markuptools.Markup((command1, command2))

    parser = LilyPondParser()
    result = parser(format(markup, 'lilypond'))

    assert isinstance(result, markuptools.Markup)
    assert format(result, 'lilypond') == format(markup, 'lilypond')


def test_lilypondparsertools_LilyPondParser__indicators__Markup_05():

    command = r'\markup { \char ##x03EE }'
    parser = LilyPondParser()
    result = parser(command)
    assert format(result, 'lilypond') == stringtools.normalize(
        r'''
        \markup {
            \char
                #1006
            }
        ''',
        )
