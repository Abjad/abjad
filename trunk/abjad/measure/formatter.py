from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions.exceptions import OverfullMeasureError
from abjad.exceptions.exceptions import UnderfullMeasureError
from abjad.rational.rational import Rational
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _invocation_closing(self):
      '''Optional class-level stop comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered stop comments.
         Set client_class.block to 'number' to print numbered stop comments.
         Analagous to open brackets for other types of container.
      '''
      result = [ ]
      block = getattr(self._client.__class__, 'block', None)
      if block == True:
         result.append('%% stop measure')
      elif block == 'number':
         measure_number = self._client.numbering.measure
         result.append('%% stop measure %s' % measure_number)
      return result

   @property
   def _invocation_opening(self):
      '''Optional class-level start comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered start comments.
         Set client_class.block to 'number' to print numbered start comments.
         Analagous to close brackets for other types of container.
      '''
      result = [ ]
      block = getattr(self._client.__class__, 'block', None)
      if block == True:
         result.append('%% start measure')
      elif block == 'number':
         measure_number = self._client.numbering.measure
         result.append('%% start measure %s' % measure_number)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      result.extend(self._client.comments._before)
      result.extend(self.before)
      result.extend(self._invocation_opening)
      result.extend(self.opening)
      result.extend(self._opening)
      result.extend(self._contents)
      result.extend(self._closing)
      result.extend(self.closing)
      result.extend(self._invocation_closing)
      result.extend(self.after)
      result.extend(self._client.comments._after)
      return '\n'.join(result)
