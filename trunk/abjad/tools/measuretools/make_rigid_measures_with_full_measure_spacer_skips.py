from abjad.components._Measure import RigidMeasure
from abjad.components.Skip import Skip
from abjad.tools import metertools
from abjad.tools.measuretools.fill_measures_in_expr_with_full_measure_spacer_skips import \
   fill_measures_in_expr_with_full_measure_spacer_skips


def make_rigid_measures_with_full_measure_spacer_skips(meters):
   r'''Make list of rigid measures with full-measure spacer skips.

   `meters` must be an iterable of Abjad meter tokens. ::

      abjad> staff = Staff(measuretools.make_rigid_measures_with_full_measure_spacer_skips([(1, 8), (5, 16), (5, 16)]))
      abjad> print staff.format
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

   .. versionchanged:: 1.1.2
      renamed ``measuretools.make( )`` to
      ``measuretools.make_rigid_measures_with_full_measure_spacer_skips( )``.
   '''

   ## check input
   if not all([metertools.is_meter_token(meter) for meter in meters]):
      raise ValueError('meters must all be Abjad meter tokens.')

   ## make measures
   measures = [RigidMeasure(meter, [ ]) for meter in meters]
   fill_measures_in_expr_with_full_measure_spacer_skips(measures)
   
   ## return measures
   return measures
