from abjad.tools import scoretemplatetools


def test_TwoStaffPianoScoreTemplate___call___01():

    template = scoretemplatetools.TwoStaffPianoScoreTemplate()
    score = template()

    r'''
    \context Score = "Two-Staff Piano Score" <<
        \context PianoStaff = "Piano Staff" <<
            \set PianoStaff.instrumentName = \markup { Piano }
            \set PianoStaff.shortInstrumentName = \markup { Pf. }
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

    assert score.lilypond_format == '\\context Score = "Two-Staff Piano Score" <<\n\t\\context PianoStaff = "Piano Staff" <<\n\t\t\\set PianoStaff.instrumentName = \\markup { Piano }\n\t\t\\set PianoStaff.shortInstrumentName = \\markup { Pf. }\n\t\t\\context Staff = "RH Staff" {\n\t\t\t\\clef "treble"\n\t\t\t\\context Voice = "RH Voice" {\n\t\t\t}\n\t\t}\n\t\t\\context Staff = "LH Staff" {\n\t\t\t\\clef "bass"\n\t\t\t\\context Voice = "LH Voice" {\n\t\t\t}\n\t\t}\n\t>>\n>>'
