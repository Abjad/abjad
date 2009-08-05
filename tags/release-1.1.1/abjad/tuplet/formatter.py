from abjad.container.formatter import _ContainerFormatter
from abjad.tuplet.slots import _TupletFormatterSlotsInterface


class _TupletFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self.label = None
      self._slots = _TupletFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _fraction(self):
      tuplet = self._client
      if not tuplet.duration._binary:
         if not tuplet.invisible:
            return r'\fraction '
      else:
         return ''

   ## PUBLIC ATTRIBUTES ##

   @property
   def slots(self):
      return self._slots

   @property
   def tuplet(self):
      return self._client
