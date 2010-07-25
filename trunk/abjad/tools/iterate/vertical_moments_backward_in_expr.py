from abjad.component import _Component
from abjad.rational import Rational
from abjad.tools.iterate.get_vertical_moment_at_prolated_offset_in_expr \
   import get_vertical_moment_at_prolated_offset_in_expr
from abjad.tools.iterate.naive_forward_in_expr import naive_forward_in_expr


def vertical_moments_backward_in_expr(governor):
   r'''.. versionadded:: 1.1.2

   Yield vertical moments forward in `governor`. ::

      abjad> score = Score([ ])
      abjad> score.append(Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))]))
      abjad> piano_staff = PianoStaff([ ])
      abjad> piano_staff.append(Staff(leaftools.make_repeated_notes(2, Rational(1, 4))))
      abjad> piano_staff.append(Staff(leaftools.make_repeated_notes(4)))
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
      abjad> for vertical_moment in iterate.vertical_moments_backward_in_expr(score):
      ...     vertical_moment.leaves
      ... 
      (Note(b', 8), Note(g', 4), Note(c', 8))
      (Note(b', 8), Note(g', 4), Note(d', 8))
      (Note(c'', 8), Note(g', 4), Note(d', 8))
      (Note(c'', 8), Note(a', 4), Note(e', 8))
      (Note(d'', 8), Note(a', 4), Note(e', 8))
      (Note(d'', 8), Note(a', 4), Note(f', 8))
      abjad> for vertical_moment in iterate.vertical_moments_backward_in_expr(piano_staff):
      ...     vertical_moment.leaves
      ... 
      (Note(g', 4), Note(c', 8))
      (Note(g', 4), Note(d', 8))
      (Note(a', 4), Note(e', 8))
      (Note(a', 4), Note(f', 8))

   .. todo:: optimize without multiple full-component traversal.

   .. versionchanged:: 1.1.2
      renamed ``iterate.vertical_moments_backward_in( )`` to
      ``iterate.vertical_moments_backward_in_expr( )``.
   '''
   from abjad.tools.verticalitytools.VerticalMoment import VerticalMoment

   moments_in_governor = [ ]
   for component in naive_forward_in_expr(governor, _Component):
      prolated_offset = component.offset.prolated.start
      if prolated_offset not in moments_in_governor:
         moments_in_governor.append(prolated_offset)
   moments_in_governor.sort( )

   for moment_in_governor in reversed(moments_in_governor):
      yield get_vertical_moment_at_prolated_offset_in_expr(
         governor, moment_in_governor)
