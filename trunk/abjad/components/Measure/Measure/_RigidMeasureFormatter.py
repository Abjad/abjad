from abjad.core import Rational
from abjad.components.Measure._MeasureFormatter import _MeasureFormatter
from abjad.exceptions import NonbinaryMeterSuppressionError
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.tools import marktools


class _RigidMeasureFormatter(_MeasureFormatter):

   def __init__(self, client):
      _MeasureFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      result = [ ]
      client = self._client
      if client.duration.nonbinary:
         result.append("\t\\scaleDurations #'(%s . %s) {" % (
            client.duration.multiplier.numerator,
            client.duration.multiplier.denominator))
         result.extend(
            ['\t' + x for x in _MeasureFormatter._contents.fget(self)])
         result.append('\t}')
      else:
         result.extend(_MeasureFormatter._contents.fget(self))
      return result

   ## PUBLIC ATTRIBUTES ##
         
   @property
   def format(self):
      from abjad.tools import marktools
      client = self._client
      effective_meter = marktools.get_effective_time_signature(self._client)
      if effective_meter.nonbinary and effective_meter.suppress:
         raise NonbinaryMeterSuppressionError
      if effective_meter.duration < client.duration.preprolated:
         raise OverfullMeasureError
      if client.duration.preprolated < effective_meter.duration:
         raise UnderfullMeasureError
      return _MeasureFormatter.format.fget(self)
