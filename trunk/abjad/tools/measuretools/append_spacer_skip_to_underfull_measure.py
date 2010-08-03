from abjad.skip import Skip
from abjad.measure.rigid.RigidMeasure import RigidMeasure


def append_spacer_skip_to_underfull_measure(rigid_measure):
   r'''.. versionadded:: 1.1.1

   Append spacer skip to underfull `measure`::

      abjad> measure = RigidMeasure((4, 12), macros.scale(4))
      abjad> measure.meter.forced = Meter(5, 12)
      abjad> measure.duration.is_underfull 
      True
      
   ::
      
      abjad> measuretools.append_spacer_skip_to_underfull_measure(measure) 
      RigidMeasure(5/12, [c'8, d'8, e'8, f'8, s1 * 1/8])
      
   ::
      
      abjad> f(measure)
      {
         \time 5/12
         \scaleDurations #'(2 . 3) {
            c'8
            d'8
            e'8
            f'8
            s1 * 1/8
         }
      }

   Append nothing to nonunderfull `measure`.

   Return `measure`.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.make_underfull_spacer_skip( )`` to
      ``measuretools.append_spacer_skip_to_underfull_measure( )``.
   '''

   assert isinstance(rigid_measure, RigidMeasure)

   if rigid_measure.duration.is_underfull:
      target_duration = rigid_measure.meter.forced.duration
      prolated_duration = rigid_measure.duration.prolated
      skip = Skip((1, 1))
      meter_multiplier = rigid_measure.meter.forced.multiplier
      new_multiplier = (target_duration - prolated_duration) / meter_multiplier
      skip.duration.multiplier = new_multiplier
      #return skip
      rigid_measure.append(skip)

   return rigid_measure
