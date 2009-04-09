from abjad.tools import metertools
from abjad.helpers.measures_populate import measures_populate
from abjad.measure.rigid.measure import RigidMeasure
from abjad.skip.skip import Skip


def measures_make(meters):
   '''Make list of skip-populated rigid measures;
      only one skip per measure, with LilyPond 
      duration multipliers, as required.'''

   assert all([metertools.is_token(meter) for meter in meters]) 

   measures = [RigidMeasure(meter, [ ]) for meter in meters]
   measures_populate(measures, 'skip')
   
   return measures
