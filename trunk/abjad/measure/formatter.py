from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions.exceptions import OverfullMeasureError
from abjad.exceptions.exceptions import UnderfullMeasureError
from abjad.rational.rational import Rational
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ### PUBLIC ATTRIBUTES ###

   @property
   def format(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
