from abjad.tools import scoretemplatetools


def test_TwoStaffPianoScoreTemplate___call___01():

    template = scoretemplatetools.TwoStaffPianoScoreTemplate()
    score = template()

    r'''
    \context Score = "Two-Staff Piano Score" <<
        \context PianoStaff = "Piano Staff" <<
            \context Staff = "RH Staff" {
                \clef "treble"
                \context Voice = "RH Voice" {
                }
            }
            \context Staff = "LH Staff" {
                \clef "bass"
                \context Voice = "LH Voice" {
                }
            }
        >>
    >>
    '''

    assert score.format == '\\context Score = "Two-Staff Piano Score" <<\n\t\\context PianoStaff = "Piano Staff" <<\n\t\t\\context Staff = "RH Staff" {\n\t\t\t\\clef "treble"\n\t\t\t\\context Voice = "RH Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "LH Staff" {\n\t\t\t\\clef "bass"\n\t\t\t\\context Voice = "LH Voice" {\n\t\t\t}\n\t\t}\n\t>>\n>>'
