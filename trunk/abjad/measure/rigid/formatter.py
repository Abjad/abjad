from abjad.exceptions.exceptions import NonbinaryMeterSuppressionError
from abjad.exceptions.exceptions import OverfullMeasureError
from abjad.exceptions.exceptions import UnderfullMeasureError
from abjad.measure.formatter import _MeasureFormatter
from abjad.rational.rational import Rational


class _RigidMeasureFormatter(_MeasureFormatter):

   def __init__(self, client):
      _MeasureFormatter.__init__(self, client)

   ### PUBLIC ATTRIBUTES ###

   @property
   def format(self):
      client = self._client
      if client.meter.effective.nonbinary and client.meter.effective.suppress:
         raise NonbinaryMeterSuppressionError
      if client.duration.preprolated > client.meter.effective.duration:
         raise OverfullMeasureError
      if client.duration.preprolated < client.meter.effective.duration:
         raise UnderfullMeasureError
      return _MeasureFormatter.format.fget(self)
