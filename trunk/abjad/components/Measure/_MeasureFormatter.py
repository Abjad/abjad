from abjad.components.Container._ContainerFormatter import _ContainerFormatter
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.components.Measure._MeasureFormatterNumberInterface import \
   _MeasureFormatterNumberInterface
from abjad.components.Measure._MeasureFormatterSlotsInterface import \
   _MeasureFormatterSlotsInterface


class _MeasureFormatter(_ContainerFormatter):
   '''Encapsulate all dynamic measure and anonymous measure
   format logic::

      abjad> measure = AnonymousMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   ::

      abjad> measure = DynamicMeasure(macros.scale(3))
      abjad> measure.formatter
      <_MeasureFormatter>

   Measure instances implement a special formatter which inherits from this base class. ::

      abjad> measure = Measure((3, 8), macros.scale(3))
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
      '''Read-only reference to measure formatter slots interface.
      '''
      return self._slots
