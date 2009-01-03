from abjad.measure.base import _Measure
from abjad.meter.meter import Meter


class DynamicMeasure(_Measure):

   def __init__(self, music = None):
      _Measure.__init__(self, music)

   ### PUBLIC ATTRIBUTES ###

   ### TODO - Notice that the dynamic production of Meter
   ###        here means that we can not use t.meter
   ###        as a grob handler. It will not work to say
   ###        t.meter.transparent = True for DyanmicMeasure.
   ### 
   ###        Solution is to give all measures, including
   ###        this DynamicMeasure, a _MeterInterface.
   ###        This _MeterInterface will both handle 
   ###        LilyPond TimeSignature grob overrides and also
   ###        possess an Abjad meter.
   
   @apply
   def meter( ):
      def fget(self):
         return Meter(self.duration.contents)
      return property(**locals( ))

   ### TODO - Implement a 'preferred denominator' attribute somehow;
   ###        idea will be to set to, say, 16 and have a total duration
   ###        of 1/2 format as 8/16 instead of 1/2.
