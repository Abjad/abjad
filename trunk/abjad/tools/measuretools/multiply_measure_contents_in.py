from abjad.meter import Meter
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import iterate


def multiply_measure_contents_in(expr, n):
   r'''Multiply contents ``n - 1`` times and adjust meter
   of every measure in `expr`::

      abjad> measure = RigidMeasure((3, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
      abjad> Beam(measure.leaves)
      abjad> f(measure)
      {
         \time 3/8
         c'8 [
         d'8
         e'8 ]
      }
      
   ::
      
      abjad> measuretools.multiply_measure_contents_in(measure, 3) 
      
   ::
      
      abjad> f(measure)
      {
         \time 9/8
         c'8 [
         d'8
         e'8 ]
         c'8 [
         d'8
         e'8 ]
         c'8 [
         d'8
         e'8 ]
      }

   .. versionchanged:: 1.1.2
      renamed ``measuretools.spin( )`` to
      ``measuretools.multiply_measure_contents_in( )``.
   '''

   from abjad.tools import containertools
   assert isinstance(n, int)
   assert n > 0

   for measure in iterate.measures_forward_in(expr):
      old_meter = measure.meter.effective
      containertools.repeat_contents_of_container(measure, n)
      old_pair = (old_meter.numerator, old_meter.denominator)
      new_pair = durtools.pair_multiply_naive(old_pair, Rational(n))
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
