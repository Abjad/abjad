from abjad.components.Container._ContainerFormatterNumberInterface import \
   _ContainerFormatterNumberInterface
from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface
from abjad.components._Component._ComponentFormatter import _ComponentFormatter


class _ContainerFormatter(_ComponentFormatter):

   def __init__(self, client):
      _ComponentFormatter.__init__(self, client)
      self._number = _ContainerFormatterNumberInterface(self)
      self._slots = _ContainerFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      '''Read-only list of tabbed lines of content.
      '''
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
