# -*- encoding: utf-8 -*-
import pytest
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
