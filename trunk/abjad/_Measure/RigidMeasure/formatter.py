from abjad.exceptions import NonbinaryMeterSuppressionError
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.measure.formatter import _MeasureFormatter
from abjad.rational import Rational


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
            client.duration.multiplier._n,
            client.duration.multiplier._d))
         result.extend(
            ['\t' + x for x in _MeasureFormatter._contents.fget(self)])
         result.append('\t}')
      else:
         result.extend(_MeasureFormatter._contents.fget(self))
      return result

   ## PUBLIC ATTRIBUTES ##
         
   @property
   def format(self):
      client = self._client
      if client.meter.effective.nonbinary and client.meter.suppress:
         raise NonbinaryMeterSuppressionError
      if client.duration.preprolated > client.meter.effective.duration:
         raise OverfullMeasureError
      if client.duration.preprolated < client.meter.effective.duration:
         raise UnderfullMeasureError
      return _MeasureFormatter.format.fget(self)
