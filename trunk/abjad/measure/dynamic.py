from abjad.measure.base import _Measure
from abjad.meter.meter import Meter


class DynamicMeasure(_Measure):

   def __init__(self, music = None):
      _Measure.__init__(self, music)

   ### PUBLIC ATTRIBUTES ###

   @apply
   def meter( ):
      def fget(self):
         return self._meter
      return property(**locals( ))

   ### TODO - Implement a 'preferred denominator' attribute somehow;
   ###        idea will be to set to, say, 16 and have a total duration
   ###        of 1/2 format as 8/16 instead of 1/2.
