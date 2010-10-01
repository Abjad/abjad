from abjad.tools.metertools import Meter
from fractions import Fraction
from abjad.tools import containertools
from abjad.tools import contexttools
from abjad.tools import metertools
from abjad.tools import componenttools
from abjad.tools.componenttools._switch import _switch
from abjad.tools.spannertools._give_dominant_to import _give_dominant_to


def fuse_measures(measures):
   r'''Fuse `measures`::

      abjad> staff = Staff(measuretools.make_rigid_measures_with_full_measure_spacer_skips([(1, 8), (2, 16)]))
      abjad> measuretools.fill_measures_in_expr_with_repeated_notes(staff, Fraction(1, 16))
      abjad> macros.diatonicize(staff)
      abjad> spannertools.BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         {
            \time 1/8
            c'16 [
            d'16
         }
         {
            \time 2/16
            e'16
            f'16 ]
         }
      }
      
   ::
      
      abjad> measuretools.fuse_measures(staff[:])
      Measure(2/8, [c'16, d'16, e'16, f'16])

   ::

      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'16 [
            d'16
            e'16
            f'16 ]
         }
      }

   Return new measure.

   Allow parent-contiguous `measures`.

   Allow outside-of-score `measures`.

   Do not define measure fusion across intervening container boundaries.

   Calculate best new time signature.

   Instantiate new measure.

   Give `measures` contents to new measure.

   Give `measures` dominant spanners to new measure.

   Give `measures` parentage to new measure.

   Leave `measures` empty, unspanned and outside-of-score.

   .. versionchanged:: 1.1.2
      renamed ``fuse.measures_by_reference( )`` to
      ``measuretools.fuse_measures( )``.
   '''
   from abjad.components.Measure import Measure
   from abjad.tools import componenttools

   assert componenttools.all_are_contiguous_components_in_same_parent(measures,
      klasses = (Measure, ))

   if len(measures) == 0:
      return None

   ## TODO: Instantiate a new measure, even length is 1 ##

   if len(measures) == 1:
      return measures[0]

   parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components(measures)

   old_denominators = [ ]
   new_duration = Fraction(0)
   for measure in measures:
      effective_meter = contexttools.get_effective_time_signature(measure)
      old_denominators.append(effective_meter.denominator)
      new_duration += effective_meter.duration

   new_meter = metertools.duration_and_possible_denominators_to_meter(
      new_duration, old_denominators)

   music = [ ]
   for measure in measures:
      ## scale before reassignment to prevent tie chain scale drama
      multiplier = \
         contexttools.get_effective_time_signature(measure).multiplier / new_meter.multiplier
      containertools.scale_contents_of_container(measure, multiplier)
      measure_music = measure[:]
      _switch(measure_music, None)
      #containertools.scale_contents_of_container(measure_music, multiplier)
      music += measure_music

   new_measure = Measure(new_meter, music)

   if parent is not None:
      _give_dominant_to(measures, [new_measure])

   _switch(measures, None)
   if parent is not None:
      parent.insert(start, new_measure)

   return new_measure 
