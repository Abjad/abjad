from abjad import *


def test_scoretools_make_piano_score_01( ):
   '''Works with notes.'''

   pitches = [-12, 37, -10, 27, 4, 17]
   notes = [Note(x, (1, 4)) for x in pitches]
   score = scoretools.make_piano_score(notes)

   r"""
   \new Score <<
           \new PianoStaff <<
                   \context Staff = "treble" {
                           \clef "treble"
                           r4
                           cs''''4
                           r4
                           ef'''4
                           e'4
                           f''4
                   }
                   \context Staff = "bass" {
                           \clef "bass"
                           c4
                           r4
                           d4
                           r4
                           r4
                           r4
                   }
           >>
   >>
   """
   
   assert check.wf(score)
   assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tr4\n\t\t\tcs\'\'\'\'4\n\t\t\tr4\n\t\t\tef\'\'\'4\n\t\t\te\'4\n\t\t\tf\'\'4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tc4\n\t\t\tr4\n\t\t\td4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t}\n\t>>\n>>'
