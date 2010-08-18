from abjad.components.Container._ContainerFormatter import _ContainerFormatter
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.components.Measure._MeasureFormatterNumberInterface import \
   _MeasureFormatterNumberInterface
from abjad.components.Measure._MeasureFormatterSlotsInterface import \
   _MeasureFormatterSlotsInterface
from abjad.core import Rational


class _MeasureFormatter(_ContainerFormatter):
   '''Encapsulate all
   :class:`~abjad.components.Measure.dynamic.measure.DynamicMeasure` and
   :class:`~abjad.components.Measure.anonymous.AnonymousMeasure.AnonymousMeasure` 
   format logic. ::

      abjad> measure = AnonymousMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   ::

      abjad> measure = DynamicMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   :class:`~abjad.components.Measure.rigid.measure.RigidMeasure` instances implement
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
      :class:`~abjad.components.Measure.slots._MeasureFormatterSlotsInterface`.'''

      return self._slots
