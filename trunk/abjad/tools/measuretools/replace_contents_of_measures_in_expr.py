from abjad.components.Measure import Measure
from abjad.tools.measuretools.append_spacer_skips_to_underfull_measures_in_expr import append_spacer_skips_to_underfull_measures_in_expr
from abjad.tools.measuretools.get_next_measure_from_component import get_next_measure_from_component


def replace_contents_of_measures_in_expr(expr, new_contents):
   r'''.. versionadded:: 1.1.1

   Replace contents of measures in `expr` with `new_contents`::

      abjad> staff = Staff(measuretools.make_rigid_measures_with_full_measure_spacer_skips([(1, 8), (3, 16)]))
      abjad> f(staff)
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
      
      abjad> notes = macros.scale(4, Rational(1, 16))
      abjad> measuretools.replace_contents_of_measures_in_expr(staff, notes) 
      [Measure(1/8, [c'16, d'16]), Measure(3/16, [e'16, f'16, s1 * 1/16])]
      
   ::
      
      abjad> f(staff)
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

   Pad extra space at end of measures with spacer skip.

   If not enough measures raise stop iteration.

   Return measures iterated.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.overwrite_contents( )`` to
      ``measuretools.replace_contents_of_measures_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.replace_measure_contents_in( )`` to
      ``measuretools.replace_contents_of_measures_in_expr( )``.
   '''

   ## init return list
   result = [ ]

   ## get first measure and first meter
   cur_measure = get_next_measure_from_component(expr) 
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
         #cur_measure.meter.forced = cur_meter
         cur_measure._attach_explicit_meter(cur_meter)
         append_spacer_skips_to_underfull_measures_in_expr([cur_measure])
         cur_measure = get_next_measure_from_component(cur_measure)
         if cur_measure is None:
            raise StopIteration
         result.append(cur_measure)
         cur_meter = cur_measure.meter.effective
         del(cur_measure[:])

   ## restore last iterated measure
   #cur_measure.meter.forced = cur_meter
   cur_measure._attach_explicit_meter(cur_meter)
   append_spacer_skips_to_underfull_measures_in_expr(cur_measure)

   ## return iterated measures
   return result
