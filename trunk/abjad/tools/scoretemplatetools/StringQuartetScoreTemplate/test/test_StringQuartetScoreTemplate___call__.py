from abjad.tools import scoretemplatetools


def test_StringQuartetScoreTemplate___call___01():

    template = scoretemplatetools.StringQuartetScoreTemplate()
    score = template()

    r'''
    \context Score = "String Quartet Score" <<
        \context StaffGroup = "String Quartet Staff Group" <<
            \context Staff = "First Violin Staff" {
                \clef "treble"
                \context Voice = "First Violin Voice" {
                }
            }
            \context Staff = "Second Violin Voice" {
                \clef "treble"
            }
            \context Staff = "Viola Staff" {
                \clef "alto"
            }
            \context Staff = "Cello Staff" {
                \clef "bass"
            }
        >>
    >>
    '''

    assert score.format == '\\context Score = "String Quartet Score" <<\n\t\\context StaffGroup = "String Quartet Staff Group" <<\n\t\t\\context Staff = "First Violin Staff" {\n\t\t\t\\clef "treble"\n\t\t\t\\context Voice = "First Violin Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "Second Violin Voice" {\n\t\t\t\\clef "treble"\n\t\t}\n\t\t\\context Staff = "Viola Staff" {\n\t\t\t\\clef "alto"\n\t\t}\n\t\t\\context Staff = "Cello Staff" {\n\t\t\t\\clef "bass"\n\t\t}\n\t>>\n>>'
