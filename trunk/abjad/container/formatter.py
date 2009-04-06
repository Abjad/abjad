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
   def container(self):
      return self._client

   @property
   def number(self):
      return self._number

   @property
   def slots(self):
      return self._slots

   @property
   def wrapper(self):
      result = [ ]
      result.extend(self.slots.slot_1)
      result.extend(self.slots.slot_2)
      result.extend(self.slots.slot_3)
      component = self._client
      heart = '\t%%%%%% %s components omitted %%%%%%' % len(component)
      result.extend(['', heart, ''])
      result.extend(self.slots.slot_5)
      result.extend(self.slots.slot_6)
      result.extend(self.slots.slot_7)
      result = '\n'.join(result)
      return result
