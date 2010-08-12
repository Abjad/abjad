from abjad.components._Measure import _Measure
from abjad.spanners import BeamSpanner


def apply_beam_spanner_to_measure(measure):
   r'''.. versionadded:: 1.1.2

   Apply beam spanner to `measure`::

      abjad> measure = RigidMeasure((2, 8), macros.scale(2))
      abjad> f(measure)
      {
         \time 2/8
         c'8
         d'8
      }
      
   ::
      
      abjad> measuretools.apply_beam_spanner_to_measure(measure)
      BeamSpanner(|2/8(2)|)
      
   ::
      
      abjad> f(measure)
      {
         \time 2/8
         c'8 [
         d'8 ]
      }

   Return beam spanner.
   '''

   ## check measure type
   if not isinstance(measure, _Measure):
      raise TypeError('must be measure: %s' % measure)

   ## apply beam spanner to measure
   beam = BeamSpanner(measure)

   ## return beam spanner
   return beam
