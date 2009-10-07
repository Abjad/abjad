from abjad.tools import scoretools
from abjad.tools.io.show import show


def show_leaves(leaves, template = None, title = None, suppress_pdf = False):
   r""".. versionadded:: 1.1.2

   Split `leaves` into treble and bass parts across a temporary
   piano staff and then show the resulting score.

   Return temporary score. ::
   
      abjad> leaves = construct.leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
      abjad> score = leaftools.show_leaves(leaves)
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

   Useful when working with mixed notes, rests and chords that have not
   yet been added to score.
   """

   score, treble, bass = scoretools.make_piano_sketch_score(leaves)
   show(score, template = template, title = title, suppress_pdf = suppress_pdf)

   return score
