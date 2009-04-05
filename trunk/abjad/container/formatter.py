from abjad.container.number import _ContainerFormatterNumberInterface
from abjad.container.slots import _ContainerFormatterSlotsInterface
from abjad.component.formatter import _ComponentFormatter


class _ContainerFormatter(_ComponentFormatter):

   def __init__(self, client):
      _ComponentFormatter.__init__(self, client)
      self._number = _ContainerFormatterNumberInterface(self)
      self._slots = _ContainerFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def number(self):
      return self._number

   @property
   def slots(self):
      return self._slots
