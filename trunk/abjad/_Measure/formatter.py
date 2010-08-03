from abjad.container.formatter import _ContainerFormatter
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.measure.number import _MeasureFormatterNumberInterface
from abjad.measure.slots import _MeasureFormatterSlotsInterface
from abjad.rational import Rational
from abjad.tuplet import FixedMultiplierTuplet


class _MeasureFormatter(_ContainerFormatter):
   '''Encapsulate all
   :class:`~abjad.measure.dynamic.measure.DynamicMeasure` and
   :class:`~abjad.measure.anonymous.AnonymousMeasure.AnonymousMeasure` 
   format logic. ::

      abjad> measure = AnonymousMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   ::

      abjad> measure = DynamicMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   :class:`~abjad.measure.rigid.measure.RigidMeasure` instances implement
   a special formatter which inherits from this base class. ::

      abjad> measure = RigidMeasure((3, 8), macros.scale(3))
      abjad> measure.formatter
      <_RigidMeasureFormatter>
   '''

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._number = _MeasureFormatterNumberInterface(self)
      self._slots = _MeasureFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slots(self):
      '''Read-only reference to 
      :class:`~abjad.measure.slots._MeasureFormatterSlotsInterface`.'''

      return self._slots
