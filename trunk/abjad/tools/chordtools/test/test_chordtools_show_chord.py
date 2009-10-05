from abjad import *


def test_chordtools_show_chord_01( ):

   chord = Chord([-29, -21, -18, -15, -11, 10, 12, 14, 20, 23, 28, 29], (1, 4))
   score = chordtools.show_chord(chord, suppress_pdf = True)
   
   r"""
   \new Score <<
        \new PianoStaff <<
                \new Staff {
                        {
                                \override Staff.TimeSignature #'stencil = ##f
                                \time 1/4
                                <bf' c'' d'' af'' b'' e''' f'''>4
                                \revert Staff.TimeSignature #'stencil
                        }
                }
                \new Staff {
                        \clef "bass"
                        {
                                \override Staff.TimeSignature #'stencil = ##f
                                \time 1/4
                                <g,, ef, fs, a, cs>4
                                \revert Staff.TimeSignature #'stencil
                        }
                }
        >>
   >>
   """

   assert check.wf(score)
   assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\new Staff {\n\t\t\t{\n\t\t\t\t\\override Staff.TimeSignature #\'stencil = ##f\n\t\t\t\t\\time 1/4\n\t\t\t\t<bf\' c\'\' d\'\' af\'\' b\'\' e\'\'\' f\'\'\'>4\n\t\t\t\t\\revert Staff.TimeSignature #\'stencil\n\t\t\t}\n\t\t}\n\t\t\\new Staff {\n\t\t\t\\clef "bass"\n\t\t\t{\n\t\t\t\t\\override Staff.TimeSignature #\'stencil = ##f\n\t\t\t\t\\time 1/4\n\t\t\t\t<g,, ef, fs, a, cs>4\n\t\t\t\t\\revert Staff.TimeSignature #\'stencil\n\t\t\t}\n\t\t}\n\t>>\n>>'
