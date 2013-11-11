# -*- encoding: utf-8 -*-
from abjad import *
import pytest


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
    assert len(result) == 2

    assert systemtools.TestManager.compare(
        result[0],
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

    assert systemtools.TestManager.compare(
        result[1],
        r'''
        \score {
            \new Staff {
                c'4 ^ \markup { This is a global variable. }
            }
        }
        '''
        )

    r'''
    \score {
        \new Staff {
            c'4 ^ \markup { This is a global variable. }
        }
    }
    '''
