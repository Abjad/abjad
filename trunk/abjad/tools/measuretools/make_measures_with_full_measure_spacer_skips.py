from abjad.tools.measuretools.Measure import Measure
from abjad.tools import metertools
from abjad.tools.measuretools.fill_measures_in_expr_with_full_measure_spacer_skips import fill_measures_in_expr_with_full_measure_spacer_skips


def make_measures_with_full_measure_spacer_skips(meters):
   r'''Make rigid measures with full-measure spacer skips from `meters`::

      abjad> measures = measuretools.make_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16)])

   ::

      abjad> staff = Staff(measures)
      abjad> f(staff)
      \new Staff {
              {
                      \time 1/8
                      s1 * 1/8
              }
              {
                      \time 5/16
                      s1 * 5/16
              }
              {
                      \time 5/16
                      s1 * 5/16
              }
      }

   Return list of rigid measures.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.make( )`` to
      ``measuretools.make_measures_with_full_measure_spacer_skips( )``.

   .. versionchanged:: 1.1.2
      renamed ``measuretools.make_rigid_measures_with_full_measure_spacer_skips( )`` to
      ``measuretools.make_measures_with_full_measure_spacer_skips( )``.
   '''
   from abjad.tools.skiptools.Skip import Skip

   ## check input
   if not all([metertools.is_meter_token(meter) for meter in meters]):
      raise ValueError('meters must all be Abjad meter tokens.')

   ## make measures
   measures = [Measure(meter, [ ]) for meter in meters]
   fill_measures_in_expr_with_full_measure_spacer_skips(measures)
   
   ## return measures
   return measures
