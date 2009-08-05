from abjad.measure.rigid.measure import RigidMeasure
from abjad.tools import iterate
from remedy_underfull_measures import remedy_underfull_measures


def overwrite_contents(expr, new_contents):
   r'''.. versionadded:: 1.1.1

   Iterate measures in `expr` and replace current measure contents
   with `new_contents`.

   Pad extra space at end of measures with spacer skip.

   Return iterated measures. ::

      abjad> staff = Staff(measuretools.make([(1, 8), (3, 16)]))
      abjad> print staff.format
      \new Staff {
              {
                      \time 1/8
                      s1 * 1/8
              }
              {
                      \time 3/16
                      s1 * 3/16
              }
      }

   ::

      abjad> notes = construct.scale(4, Rational(1, 16))
      abjad> measuretools.overwrite_contents(t, notes)
      [RigidMeasure(1/8, [c'16, d'16]), RigidMeasure(3/16, [e'16, f'16, s1 * 1/16])]
      abjad> print staff.format
      \new Staff {
              {
                      \time 1/8
                      c'16
                      d'16
              }
              {
                      \time 3/16
                      e'16
                      f'16
                      s1 * 1/16
              }
      }

   Preserve duration of all measures.

   Skip measures that are too small.

   If not enough measures, raise :exc:`StopIteration`.
   '''

   ## init return list
   result = [ ]

   ## get first measure and first meter
   cur_measure = iterate.measure_next(expr) 
   result.append(cur_measure)
   cur_meter = cur_measure.meter.effective
   del(cur_measure[:])

   ## iterate new contents
   while new_contents:

      ## find candidate duration of new element plus current measure 
      cur_element = new_contents[0]
      multiplier = cur_meter.multiplier
      preprolated_duration = cur_element.duration.preprolated
      prolated_duration = multiplier * preprolated_duration
      candidate_duration = cur_measure.duration.prolated + prolated_duration

      ## if new element fits in current measure
      if candidate_duration <= cur_meter.duration:
         cur_element = new_contents.pop(0)
         cur_measure.append(cur_element)

      ## otherwise restore currene measure and advance to next measure
      else:
         cur_measure.meter.forced = cur_meter
         remedy_underfull_measures([cur_measure])
         cur_measure = iterate.measure_next(cur_measure)
         if cur_measure is None:
            raise StopIteration
         result.append(cur_measure)
         cur_meter = cur_measure.meter.effective
         del(cur_measure[:])

   ## restore last iterated measure
   cur_measure.meter.forced = cur_meter
   remedy_underfull_measures(cur_measure)

   ## return iterated measures
   return result
