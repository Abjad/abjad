from abjad.spanners import Beam
from abjad.tools import iterate
from abjad.tools.measuretools.apply_beam_spanner_to_measure import \
   apply_beam_spanner_to_measure


def apply_beam_spanners_to_measures_in(expr):
   r'''.. versionadded:: 1.1.1

   Apply beam spanners to measures in `expr`::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8
            d'8
         }
         {
            \time 2/8
            e'8
            f'8
         }
      }
      
   ::
      
      abjad> measuretools.apply_beam_spanners_to_measures_in(staff)
      [Beam(|2/8(2)|), Beam(|2/8(2)|)]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'8 [
            d'8 ]
         }
         {
            \time 2/8
            e'8 [
            f'8 ]
         }
      }

   Return list of beams created.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.beam( )`` to
      ``measuretools.apply_beam_spanners_to_measures_in( )``.
   '''

   ## init beams created
   beams_created = [ ]

   ## apply beam spanners to measures in expr
   for measure in iterate.measures_forward_in(expr):
      beam = apply_beam_spanner_to_measure(measure)
      beams_created.append(beam)

   ## return beams created
   return beams_created
