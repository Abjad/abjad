from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions.exceptions import OverfullMeasureError
from abjad.exceptions.exceptions import UnderfullMeasureError
from abjad.measure.number import _MeasureFormatterNumberInterface
from abjad.rational.rational import Rational
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._number = _MeasureFormatterNumberInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   #def invocation_opening(self):
   def slot_2(self):
      '''Optional class-level start comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered start comments.
         Set client_class.block to 'number' to print numbered start comments.
         Analagous to close brackets for other types of container.'''
      result = [ ]
      client = self._client
      contribution = self.number._measure_contribution
      if contribution == 'comment':
         result.append('%% start measure %s' % client.numbering.measure)
      return result

   @property
   #def invocation_closing(self):
   def slot_6(self):
      '''Optional class-level stop comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered stop comments.
         Set client_class.block to 'number' to print numbered stop comments.
         Analagous to open brackets for other types of container.'''
      result = [ ]
      client = self._client
      contribution = self.number._measure_contribution
      if contribution == 'comment':
         result.append('%% stop measure %s' % client.numbering.measure)
      return result
