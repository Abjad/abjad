from abjad.measure.rigid.measure import RigidMeasure
from abjad.skip.skip import Skip
from abjad.tools import metertools
from abjad.tools.measuretools.populate import populate


def make(meters):
   '''Make list of skip-populated rigid measures;
      only one skip per measure, with LilyPond 
      duration multipliers, as required.'''

   assert all([metertools.is_token(meter) for meter in meters]) 

   measures = [RigidMeasure(meter, [ ]) for meter in meters]
   populate(measures, 'skip')
   
   return measures
