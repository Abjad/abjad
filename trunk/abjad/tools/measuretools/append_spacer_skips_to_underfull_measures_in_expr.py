from abjad.tools import componenttools
from abjad.components.Measure import Measure
from abjad.tools.measuretools.append_spacer_skip_to_underfull_measure import append_spacer_skip_to_underfull_measure


def append_spacer_skips_to_underfull_measures_in_expr(expr):
   r'''.. versionadded:: 1.1.1

   Append spacer skips to underfull measures in `expr`::

      abjad> staff = Staff(RigidMeasure((3, 8), macros.scale(3)) * 3)
      abjad> staff[1].meter.forced = metertools.Meter(4, 8)
      abjad> staff[2].meter.forced = metertools.Meter(5, 8)
      abjad> staff[1].duration.is_underfull 
      True
      abjad> staff[2].duration.is_underfull 
      True
      
   ::
      
      abjad> measuretools.append_spacer_skips_to_underfull_measures_in_expr(staff) 
      [RigidMeasure(4/8, [c'8, d'8, e'8, s1 * 1/8]), RigidMeasure(5/8, [c'8, d'8, e'8, s1 * 1/4])]
      
   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 3/8
            c'8
            d'8
            e'8
         }
         {
            \time 4/8
            c'8
            d'8
            e'8
            s1 * 1/8
         }
         {
            \time 5/8
            c'8
            d'8
            e'8
            s1 * 1/4
         }
      }

   Return measures treated.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.remedy_underfull_measures( )`` to
      ``measuretools.append_spacer_skips_to_underfull_measures_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.append_spacer_skips_to_underfull_measures_in( )`` to
      ``measuretools.append_spacer_skips_to_underfull_measures_in_expr( )``.
   '''

   treated_measures = [ ]
   for rigid_measure in componenttools.iterate_components_forward_in_expr(expr, RigidMeasure):
      if rigid_measure.duration.is_underfull:
         #spacer_skip = append_spacer_skip_to_underfull_measure(rigid_measure)
         #rigid_measure.append(spacer_skip)
         append_spacer_skip_to_underfull_measure(rigid_measure)
         treated_measures.append(rigid_measure)
   return treated_measures
