from abjad.marks import Meter
from abjad.core import Rational
from abjad.tools import durtools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def multiply_contents_of_measures_in_expr(expr, n):
   r'''Multiply contents ``n - 1`` times and adjust meter
   of every measure in `expr`::

      abjad> measure = RigidMeasure((3, 8), macros.scale(3))
      abjad> spannertools.BeamSpanner(measure.leaves)
      abjad> f(measure)
      {
         \time 3/8
         c'8 [
         d'8
         e'8 ]
      }
      
   ::
      
      abjad> measuretools.multiply_contents_of_measures_in_expr(measure, 3) 
      
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
      ``measuretools.multiply_contents_of_measures_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.multiply_measure_contents_in( )`` to
      ``measuretools.multiply_contents_of_measures_in_expr( )``.
   '''

   from abjad.tools import containertools
   assert isinstance(n, int)
   assert 0 < n

   for measure in iterate_measures_forward_in_expr(expr):
      old_meter = measure.meter.effective
      containertools.repeat_contents_of_container(measure, n)
      old_pair = (old_meter.numerator, old_meter.denominator)
      new_pair = durtools.multiply_duration_pair(old_pair, Rational(n))
      new_meter = Meter(new_pair)
      measure.meter.forced = new_meter
