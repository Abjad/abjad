from abjad.container.formatter import _ContainerFormatter
#from abjad.helpers.rational_as_fraction import _rational_as_fraction
from abjad.tuplet.slots import _TupletFormatterSlotsInterface


class _TupletFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self.label = None
      self._slots = _TupletFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def fraction(self):
      if not self._client.duration._binary:
         if not self._client.invisible:
            return r'\fraction '
      else:
         return ''

   @property
   def slots(self):
      return self._slots
