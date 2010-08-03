from abjad._Measure import RigidMeasure
from abjad.Skip import Skip
from abjad.tools import metertools
from abjad.tools.measuretools.populate import populate


def make(meters):
   r'''Make list of skip-populated rigid measures.

   `meters` must be an iterable of Abjad meter tokens. ::

      abjad> staff = Staff(measuretools.make([(1, 8), (5, 16), (5, 16)]))
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
   '''

   ## check input
   if not all([metertools.is_meter_token(meter) for meter in meters]):
      raise ValueError('meters must all be Abjad meter tokens.')

   ## make measures
   measures = [RigidMeasure(meter, [ ]) for meter in meters]
   populate(measures, 'skip')
   
   ## return measures
   return measures
