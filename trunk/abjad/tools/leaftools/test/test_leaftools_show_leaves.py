from abjad import *


def test_leaftools_show_leaves_01( ):

   leaves = construct.leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
   score = leaftools.show_leaves(leaves, suppress_pdf = True)

   r'''
   \new Score <<
           \new PianoStaff <<
                   \context Staff = "treble" {
                           \clef "treble"
                           r4
                           cs'4
                           <g' a''>4
                           r4
                   }
                   \context Staff = "bass" {
                           \clef "bass"
                           r4
                           r4
                           <c, d,>4
                           r4
                   }
           >>
   >>
   '''

   assert check.wf(score)
   assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tr4\n\t\t\tcs\'4\n\t\t\t<g\' a\'\'>4\n\t\t\tr4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tr4\n\t\t\tr4\n\t\t\t<c, d,>4\n\t\t\tr4\n\t\t}\n\t>>\n>>'
