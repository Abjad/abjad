# -*- coding: utf-8 -*-
import abjad
import pytest


@pytest.mark.skip('Pending 2.19.24 update.')
def test_lilypondparsertools_LilyPondParser__lilypondfile__HeaderBlock_01():
    string = r'''
    globalvariable = "This is a global variable."
    \header {
        globalvariable = "This abjad.overrides the global variable"
        localvariable = "and this is a local variable."
        something = #4
        title = \markup { \globalvariable \localvariable }
    }
    \score {
        \new Staff { c'4 ^ \markup { \globalvariable } }
    }
    '''
    result = parse(string)
    assert isinstance(result, abjad.LilyPondFile)
    assert len(result.items) == 2
    assert format(result.items[0]) == abjad.String.normalize(
        r'''
        \header {
            globalvariable = #"This abjad.overrides the global variable"
            localvariable = #"and this is a local variable."
            something = #4
            title = \markup {
                "This abjad.overrides the global variable"
                "and this is a local variable."
                }
        }
        '''
        )
    assert format(result.items[1]) == abjad.String.normalize(
        r'''
        \score {
            \new Staff {
                c'4 ^ \markup { This is a global variable. }
            }
        }
        '''
        )


@pytest.mark.skip('Pending 2.19.24 update.')
def test_lilypondparsertools_LilyPondParser__lilypondfile__HeaderBlock_02():
    string = r'''
    \header {
        composername = "Foo von Bar"
        composer = \markup { by \bold \composername }
        title = \markup { The ballad of \composername }
        tagline = \markup { "" }
    }
    {
        c'1
    }
    '''
    result = parse(string)
    assert isinstance(result, abjad.LilyPondFile)
    assert len(result.items) == 2
    assert format(result.items[0]) == abjad.String.normalize(
        r'''
        \header {
            composer = \markup {
                by
                \bold
                    "Foo von Bar"
                }
            composername = #"Foo von Bar"
            tagline = ##f
            title = \markup {
                The
                ballad
                of
                "Foo von Bar"
                }
        }
        ''')
    assert format(result.items[1]) == abjad.String.normalize(
        r'''
        {
            c'1
        }
        ''')
