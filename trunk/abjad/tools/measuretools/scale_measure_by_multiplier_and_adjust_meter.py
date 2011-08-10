from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import durtools
from abjad.tools import mathtools


def scale_measure_by_multiplier_and_adjust_meter(measure, multiplier = 1):
   r'''.. versionadded:: 2.0

   Scale `measure` by `multiplier` and adjust meter::

      abjad> t = Measure((3, 8), "c'8 d'8 e'8")
      abjad> measuretools.scale_measure_by_multiplier_and_adjust_meter(t, Duration(2, 3))
      Measure(3/12, [c'8, d'8, e'8])

   ::

      abjad> f(t)
      {
           \time 3/12
           \scaleDurations #'(2 . 3) {
                   c'8
                   d'8
                   e'8
           }
      }

   Return `measure`.
   '''

   from abjad.tools import containertools

   if multiplier == 0:
      raise ZeroDivisionError

   old_meter = contexttools.get_effective_time_signature(measure)
   old_pair = (old_meter.numerator, old_meter.denominator)
   old_multiplier = old_meter.multiplier
   old_multiplier_pair = (old_multiplier.numerator, old_multiplier.denominator)

   multiplied_pair = durtools.multiply_duration_pair(old_multiplier_pair, multiplier)
   reduced_pair = durtools.multiply_duration_pair_and_reduce_factors(
      old_multiplier_pair, multiplier)

   if reduced_pair != multiplied_pair:
      new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
         old_pair, multiplier)      
      new_meter = contexttools.TimeSignatureMark(new_pair)
      contexttools.detach_time_signature_mark_attached_to_component(measure)
      new_meter.attach_mark(measure)
      remaining_multiplier = durtools.Duration(*reduced_pair)
      if remaining_multiplier != durtools.Duration(1):
         containertools.scale_contents_of_container(measure, remaining_multiplier)
   elif componenttools.all_are_components_scalable_by_multiplier(measure[:], multiplier):
      containertools.scale_contents_of_container(measure, multiplier)
      if old_meter.is_nonbinary or not mathtools.is_nonnegative_integer_power_of_two(multiplier):
         new_pair = durtools.multiply_duration_pair_and_reduce_factors(old_pair, multiplier)
      ## multiplier is a negative power of two, like 1/2, 1/4, etc.
      elif multiplier < durtools.Duration(0):
         new_pair = durtools.multiply_duration_pair(old_pair, multiplier)
      ## multiplier is a nonnegative power of two, like 0, 1, 2, 4, etc.
      elif durtools.Duration(0) < multiplier:
         new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
            old_pair, multiplier)
      elif multiplier == durtools.Duration(0):
         raise ZeroDivisionError
      new_meter = contexttools.TimeSignatureMark(new_pair)
      contexttools.detach_time_signature_mark_attached_to_component(measure)
      new_meter.attach_mark(measure)
   else:
      new_pair = durtools.multiply_duration_pair_and_try_to_preserve_numerator(
         old_pair, multiplier)
      new_meter = contexttools.TimeSignatureMark(new_pair)
      contexttools.detach_time_signature_mark_attached_to_component(measure)
      new_meter.attach_mark(measure)
      remaining_multiplier = multiplier / new_meter.multiplier
      if remaining_multiplier != durtools.Duration(1):
         containertools.scale_contents_of_container(measure, remaining_multiplier)
   return measure
