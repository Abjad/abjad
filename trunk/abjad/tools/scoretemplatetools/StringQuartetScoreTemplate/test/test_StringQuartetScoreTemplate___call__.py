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
            \context Staff = "Second Violin Staff" {
                \clef "treble"
                \context Voice = "Second Violin Voice" {
                }
            }
            \context Staff = "Viola Staff" {
                \clef "alto"
                \context Voice = "Viola Voice" {
                }
            }
            \context Staff = "Cello Staff" {
                \clef "bass"
                \context Voice = "Cello Voice" {
                }
            }
        >>
    >>
    '''

    assert score.format == '\\context Score = "String Quartet Score" <<\n\t\\context StaffGroup = "String Quartet Staff Group" <<\n\t\t\\context Staff = "First Violin Staff" {\n\t\t\t\\clef "treble"\n\t\t\t\\context Voice = "First Violin Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "Second Violin Staff" {\n\t\t\t\\clef "treble"\n\t\t\t\\context Voice = "Second Violin Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "Viola Staff" {\n\t\t\t\\clef "alto"\n\t\t\t\\context Voice = "Viola Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "Cello Staff" {\n\t\t\t\\clef "bass"\n\t\t\t\\context Voice = "Cello Voice" {\n\t\t\t}\n\t\t}\n\t>>\n>>'
