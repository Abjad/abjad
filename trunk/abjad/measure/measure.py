from .. containers.container import Container
from .. containers.duration import _ContainerDurationInterface
from formatter import MeasureFormatter
from .. helpers.hasname import hasname
from meter import Meter

class Measure(Container):

   def __init__(self, meter = None, music = [ ]):
      Container.__init__(self, music)
      self._duration = _ContainerDurationInterface(self)
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
      return self._duration
