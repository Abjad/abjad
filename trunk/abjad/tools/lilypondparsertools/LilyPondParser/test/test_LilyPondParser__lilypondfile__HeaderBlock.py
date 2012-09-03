from abjad import *
import py


def test_LilyPondParser__lilypondfile__HeaderBlock_01():

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

    result = p(string)

    assert isinstance(result, lilypondfiletools.LilyPondFile)
    assert len(result) == 2

    assert result[0].lilypond_format == '\\header {\n\tglobalvariable = #"This overrides the global variable"\n\tlocalvariable = #"and this is a local variable."\n\tsomething = #4\n\ttitle = \\markup { "This overrides the global variable" "and this is a local variable." }\n}'

    r'''
    \header {
        globalvariable = #"This overrides the global variable"
        localvariable = #"and this is a local variable."
        something = #4
        title = \markup { "This overrides the global variable" "and this is a local variable." }
    }
    '''

    assert result[1].lilypond_format == '\\score {\n\t\\new Staff {\n\t\tc\'4 ^ \\markup { This is a global variable. }\n\t}\n}'

    r'''
    \score {
        \new Staff {
            c'4 ^ \markup { This is a global variable. }
        }
    }
    '''
