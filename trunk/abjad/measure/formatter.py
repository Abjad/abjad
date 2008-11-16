from abjad.containers.formatter import _ContainerFormatter
from abjad.rational.rational import Rational
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   @property
   def _meter(self):
      result = [ ]
      if self._client.meter:
         result.extend(['\t' + x for x in self._client.meter._before])
      if self._client.meter and not self._client.meter.hide:
         result.append('\t' + self._client.meter.lily)
      return result

   @property
   def lily(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._meter)
      #if self._client.nonbinary:
      #if self._client.duration.nonbinary:
      #if self._client.duration.multiplier != Rational(1, 1):
      if self._client.duration.compression != Rational(1, 1):
         #multiplier = self._client.duration.multiplier
         compression = self._client.duration.compression
         if len(self._client):
            ### TODO - may be dangerous; run tests; write tests
            measure_music = self._client[ : ]
            for x in measure_music:
               x._parent = None
            tuplet = FixedMultiplierTuplet(
               #self._client.duration.multiplier, measure_music)
               #self._client.duration.multiplier, measure_music)
               #multiplier, measure_music)
               compression, measure_music)
            tuplet.invisible = True
            result.extend(['\t' + x for x in tuplet.formatter._pieces])
            for x in measure_music:
               x._parent = self._client
      else:
         result.extend(self.opening)
         result.extend(self._opening)
         result.extend(self._contents)
         result.extend(self._closing)
         result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
