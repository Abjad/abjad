from abjad import *
from experimental import *


def test_Quantizer___call___01():

    ms = [1500, -1000, 1000, 1000, -1000, 1000, -1000, 500]
    seq = quantizationtools.QEventSequence.from_millisecond_durations(ms)
    q = quantizationtools.Quantizer()

    result = q(seq)

    assert isinstance(result, Voice)
    assert result.prolated_duration == 2

    score = Score([Staff([result])])

    r'''
    \new Score <<
        \new Staff {
            \new Voice {
                {
                    \time 4/4
                    \tempo 4=60
                    c'4 ~
                    c'8
                    r8 ~
                    r8
                    c'8 ~
                    c'8
                    c'8 ~
                }
                {
                    c'8
                    r8 ~
                    r8
                    c'8 ~
                    c'8
                    r8 ~
                    r8
                    c'8
                }
            }
        }
    >>
    '''

    assert score.lilypond_format == "\\new Score <<\n\t\\new Staff {\n\t\t\\new Voice {\n\t\t\t{\n\t\t\t\t\\time 4/4\n\t\t\t\t\\tempo 4=60\n\t\t\t\tc'4 ~\n\t\t\t\tc'8\n\t\t\t\tr8 ~\n\t\t\t\tr8\n\t\t\t\tc'8 ~\n\t\t\t\tc'8\n\t\t\t\tc'8 ~\n\t\t\t}\n\t\t\t{\n\t\t\t\tc'8\n\t\t\t\tr8 ~\n\t\t\t\tr8\n\t\t\t\tc'8 ~\n\t\t\t\tc'8\n\t\t\t\tr8 ~\n\t\t\t\tr8\n\t\t\t\tc'8\n\t\t\t}\n\t\t}\n\t}\n>>"


def test_Quantizer___call___02():

    ms = [250, 1000, 1000, 1000, 750]
    seq = quantizationtools.QEventSequence.from_millisecond_durations(ms)
    q = quantizationtools.Quantizer()

    result = q(seq)

    r'''
    \new Voice {
        {
            \time 4/4
            %%% \tempo 4=60 %%%
            c'16
            c'16 ~
            c'8 ~
            c'16
            c'16 ~
            c'8 ~
            c'16
            c'16 ~
            c'8 ~
            c'16
            c'16 ~
            c'8
        }
    }
    '''

    assert result.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 4/4\n\t\t%%% \\tempo 4=60 %%%\n\t\tc'16\n\t\tc'16 ~\n\t\tc'8 ~\n\t\tc'16\n\t\tc'16 ~\n\t\tc'8 ~\n\t\tc'16\n\t\tc'16 ~\n\t\tc'8 ~\n\t\tc'16\n\t\tc'16 ~\n\t\tc'8\n\t}\n}"


def test_Quantizer___call___03():

    q_schema = quantizationtools.BeatwiseQSchema(
        {'search_tree': quantizationtools.SimpleSearchTree({2: None})},
        {'search_tree': quantizationtools.SimpleSearchTree({3: None})},
        {'search_tree': quantizationtools.SimpleSearchTree({5: None})},
        {'search_tree': quantizationtools.SimpleSearchTree({7: None})},
        )
    ms = [250, 250, 250, 250] * 4
    seq = quantizationtools.QEventSequence.from_millisecond_durations(ms)
    q = quantizationtools.Quantizer()

    result = q(seq, q_schema=q_schema)

    r'''
    \new Voice {
        \grace {
            c'16
        }
        %%% \tempo 4=60 %%%
        c'8
        \grace {
            c'16
        }
        c'8
        \times 2/3 {
            c'8
            \grace {
                c'16
            }
            c'8
            c'8
        }
        \times 4/5 {
            c'16
            c'16
            c'16 ~
            c'16
            c'16
        }
        \times 4/7 {
            c'16 ~
            c'16
            c'16
            c'16 ~
            c'16
            c'16 ~
            c'16
        }
    }
    '''

    assert result.lilypond_format == "\\new Voice {\n\t\\grace {\n\t\tc'16\n\t}\n\t%%% \\tempo 4=60 %%%\n\tc'8\n\t\\grace {\n\t\tc'16\n\t}\n\tc'8\n\t\\times 2/3 {\n\t\tc'8\n\t\t\\grace {\n\t\t\tc'16\n\t\t}\n\t\tc'8\n\t\tc'8\n\t}\n\t\\times 4/5 {\n\t\tc'16\n\t\tc'16\n\t\tc'16 ~\n\t\tc'16\n\t\tc'16\n\t}\n\t\\times 4/7 {\n\t\tc'16 ~\n\t\tc'16\n\t\tc'16\n\t\tc'16 ~\n\t\tc'16\n\t\tc'16 ~\n\t\tc'16\n\t}\n}"
