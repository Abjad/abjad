from abjad.exceptions.exceptions import NonbinaryMeterSuppressionError
from abjad.exceptions.misfilledmeasure import MisfilledMeasureError
from abjad.measure.formatter import _MeasureFormatter
from abjad.rational.rational import Rational


class _RigidMeasureFormatter(_MeasureFormatter):

   def __init__(self, client):
      _MeasureFormatter.__init__(self, client)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _processedContents(self):
#      result = [ ]
#      if self._client.full:
#         result.extend(self._contents)
#      else:
#         raise MisfilledMeasureError
#      return result
      return self._contents

   @property
   def format(self):
      client = self._client
      if client.meter.effective.nonbinary and client.meter.effective.suppress:
         raise NonbinaryMeterSuppressionError
      if not client.full:
         raise MisfilledMeasureError
      return _MeasureFormatter.format.fget(self)
