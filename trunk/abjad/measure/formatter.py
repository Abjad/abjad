from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions.exceptions import OverfullMeasureError
from abjad.exceptions.exceptions import UnderfullMeasureError
from abjad.measure.number import _MeasureFormatterNumberInterface
from abjad.measure.slots import _MeasureFormatterSlotsInterface
from abjad.rational import Rational
from abjad.tuplet.fm.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._number = _MeasureFormatterNumberInterface(self)
      self._slots = _MeasureFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slots(self):
      return self._slots
