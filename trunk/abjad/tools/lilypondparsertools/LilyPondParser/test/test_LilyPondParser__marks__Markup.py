from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__Markup_01():
    target = Staff([Note(0, 1)])
    markuptools.Markup('hello!', Up)(target[0])

    r'''\new Staff {
        c'1 ^ \markup { hello! }
    }
    '''

    input = r'''\new Staff { c'1 ^ "hello!" }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(markuptools.get_markup_attached_to_component(result[0]))


def test_LilyPondParser__marks__Markup_02():

    target = Staff([Note(0, (1, 4))])
    markuptools.Markup(['X', 'Y', 'Z', 'a b c'], Down)(target[0])

    r'''\new Staff {
        c'4
            _ \markup {
                X
                Y
                Z
                "a b c"
                }
    }
    '''

    input = r'''\new Staff { c' _ \markup { X Y Z "a b c" } }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(markuptools.get_markup_attached_to_component(result[0]))


def test_LilyPondParser__marks__Markup_03():
    '''Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    '''

    target = Staff([Note(0, (1, 4)), Note(2, (1, 4))])
    markuptools.Markup('hello', Up)(target[0])
    marktools.Articulation('.')(target[0])

    r'''\new Staff {
        c'4 -\staccato ^ \markup { hello }
        d'4
    }
    '''

    input = r'''\new Staff { c' ^ \markup { hello } -. d' }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.lilypond_format == result.lilypond_format and target is not result
    assert 1 == len(markuptools.get_markup_attached_to_component(result[0]))


def test_LilyPondParser__markups__Markup_04():
    command1 = markuptools.MarkupCommand('bold', ['A', 'B', 'C'])
    command2 = markuptools.MarkupCommand('italic', '123')
    markup = markuptools.Markup((command1, command2))

    parser = LilyPondParser()
    result = parser(markup.lilypond_format)

    assert isinstance(result, markuptools.Markup)
    assert result.lilypond_format == markup.lilypond_format
