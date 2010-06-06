from abjad.component import _Component
from abjad.rational import Rational
from abjad.tools.iterate.VerticalMoment import VerticalMoment
from abjad.tools.iterate._new_vertical_moments_forward_in import \
   _new_vertical_moments_forward_in


def vertical_moments_forward_in(governor):
   r'''.. versionadded:: 1.1.2

   Yield vertical moments forward in `governor`. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff([FixedDurationTuplet((4, 8), construct.run(3))]))
      abjad> piano_staff = PianoStaff([ ])
      abjad> piano_staff.append(Staff(construct.run(2, Rational(1, 4))))
      abjad> piano_staff.append(Staff(construct.run(4)))
      abjad> piano_staff[1].clef.forced = Clef('bass')
      abjad> score.append(piano_staff)
      abjad> pitchtools.diatonicize(list(reversed(score.leaves)))
      abjad> f(score)
      \new Score <<
              \new Staff {
                      \times 4/3 {
                              d''8
                              c''8
                              b'8
                      }
              }
              \new PianoStaff <<
                      \new Staff {
                              a'4
                              g'4
                      }
                      \new Staff {
                              \clef "bass"
                              f'8
                              e'8
                              d'8
                              c'8
                      }
              >>
      >>
      abjad> for vertical_moment in iterate.vertical_moments_forward_in(score):
      ...     vertical_moment.leaves
      ... 
      (Note(d'', 8), Note(a', 4), Note(f', 8))
      (Note(d'', 8), Note(a', 4), Note(e', 8))
      (Note(c'', 8), Note(a', 4), Note(e', 8))
      (Note(c'', 8), Note(g', 4), Note(d', 8))
      (Note(b', 8), Note(g', 4), Note(d', 8))
      (Note(b', 8), Note(g', 4), Note(c', 8))
      abjad> for vertical_moment in iterate.vertical_moments_forward_in(piano_staff):
      ...     vertical_moment.leaves
      ... 
      (Note(a', 4), Note(f', 8))
      (Note(a', 4), Note(e', 8))
      (Note(g', 4), Note(d', 8))
      (Note(g', 4), Note(c', 8))

   .. todo:: optimize without multiple full-component traversal.
   '''

   ## OPTIMIZED DROP-IN REPLACEMENT ##
   for x in _new_vertical_moments_forward_in(governor):
      yield x
