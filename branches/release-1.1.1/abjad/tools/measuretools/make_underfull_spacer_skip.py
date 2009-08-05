from abjad.skip import Skip
from abjad.measure.rigid.measure import RigidMeasure


def make_underfull_spacer_skip(rigid_measure):
   r'''.. versionadded:: 1.1.1

   If `rigid_measure` is underfull, create spacer
   skip with the correct duration to remedy underfull measure. ::

      abjad> rigid_measure = RigidMeasure((4, 12), construct.scale(4))
      abjad> rigid_measure.meter.forced = Meter(5, 12)
      abjad> rigid_measure.duration.is_underfull
      True

   ::

      abjad> skip = measuretools.make_underfull_spacer_skip(rigid_measure)
      abjad> skip
      Skip(1 * 1/8)

   ::

      abjad> rigid_measure.append(skip)
      abjad> rigid_measure.duration.is_underfull
      False
      abjad> print rigid_measure.format
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

   If `rigid_measure` is full or overfull, return ``None``.
   '''

   assert isinstance(rigid_measure, RigidMeasure)

   if rigid_measure.duration.is_underfull:
      target_duration = rigid_measure.meter.forced.duration
      prolated_duration = rigid_measure.duration.prolated
      skip = Skip((1, 1))
      meter_multiplier = rigid_measure.meter.forced.multiplier
      new_multiplier = (target_duration - prolated_duration) / meter_multiplier
      skip.duration.multiplier = new_multiplier
      return skip
