from abjad.components.Container.formatter import _ContainerFormatter
from abjad.components.Grace.slots import _GraceFormatterSlotsInterface


class _GraceFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _GraceFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def grace(self):
      return self._client

   @property
   def slots(self):
      return self._slots
