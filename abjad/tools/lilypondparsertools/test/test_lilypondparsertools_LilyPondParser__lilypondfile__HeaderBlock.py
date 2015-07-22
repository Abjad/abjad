# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondparsertools_LilyPondParser__lilypondfile__HeaderBlock_01():
    string = r'''
    globalvariable = "This is a global variable."
    \header {
        globalvariable = "This overrides the global variable"
        localvariable = "and this is a local variable."
        title = \markup { \globalvariable \localvariable }
        something = #4
    }
    \score {
        \new Staff { c'4 ^ \markup { \globalvariable } }
    }
    '''
    result = parse(string)
    assert isinstance(result, lilypondfiletools.LilyPondFile)
    assert len(result.items) == 2
    assert systemtools.TestManager.compare(
        result.items[0],
        r'''
        \header {
            globalvariable = #"This overrides the global variable"
            localvariable = #"and this is a local variable."
            something = #4
            title = \markup {
                "This overrides the global variable"
                "and this is a local variable."
                }
        }
        '''
        )
    assert systemtools.TestManager.compare(
        result.items[1],
        r'''
        \score {
            \new Staff {
                c'4 ^ \markup { This is a global variable. }
            }
        }
        '''
        )


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
    assert isinstance(result, lilypondfiletools.LilyPondFile)
    assert len(result.items) == 2
    assert format(result.items[0]) == systemtools.TestManager.clean_string(
        r'''
        \header {
            composer = \markup {
                by
                \bold
                    "Foo von Bar"
                }
            composername = #"Foo von Bar"
            tagline = \markup {}
            title = \markup {
                The
                ballad
                of
                "Foo von Bar"
                }
        }
        ''')
    assert format(result.items[1]) == systemtools.TestManager.clean_string(
        r'''
        {
            c'1
        }
        ''')