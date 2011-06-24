from abjad.tools import contexttools
from abjad.tools import durtools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools import durtools


def multiply_contents_of_measures_in_expr(expr, n):
   r'''Multiply contents ``n - 1`` times and adjust meter
   of every measure in `expr`::

      abjad> measure = Measure((3, 8), "c'8 d'8 e'8")
      abjad> spannertools.BeamSpanner(measure.leaves)
      BeamSpanner(c'8, d'8, e'8)
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
      old_meter = contexttools.get_effective_time_signature(measure)
      containertools.repeat_contents_of_container(measure, n)
      old_pair = (old_meter.numerator, old_meter.denominator)
      new_pair = durtools.multiply_duration_pair(old_pair, durtools.Duration(n))
      measure._attach_explicit_meter(*new_pair)
