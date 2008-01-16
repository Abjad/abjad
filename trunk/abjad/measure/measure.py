from .. containers.container import Container
from .. duration.duration import Duration
from formatter import MeasureFormatter
from meter import Meter

class Measure(Container):

   def __init__(self, meter = None, music = [ ]):
      Container.__init__(self, music)
      self.formatter = MeasureFormatter(self)
      self.meter = meter

   ### REPR ###

   def __repr__(self):
      if self.meter and len(self) > 0:
         return 'Measure(%s, [%s])' % (self.meter, self._summary)
      elif self.meter:
         return 'Measure(%s)' % self.meter
      elif len(self) > 0:
         return 'Measure([%s])' % self._summary
      else:
         return 'Measure( )'

   def __str__(self):
      if self.meter and len(self) > 0:
         return '|%s, %s|' % (self.meter, self._summary)
      elif self.meter:
         return '|%s|' % self.meter
      elif len(self) > 0:
         return '|%s|' % self._summary
      else:
         return '| |'
  
   ### MANAGED PROPERTIES ###

   @apply
   def meter( ):
      def fget(self):
         return self._meter
      def fset(self, arg):
         if arg is None:
            self._meter = None
         else:
            meter = Meter(*arg)
            self._meter = meter
      return property(**locals( ))

   @property
   def duration(self):
      duration = Duration(0)
      for x in self:
         duration += x.duration
      return duration

   @property
   def duratum(self):
      result = self._parentage._prolation * self.duration
      return Duration(*result.pair)

   ### TESTS ###

   def testDuration(self):
      if self.meter:
         return self.meter.duration == self.duration
      else:
         return True
