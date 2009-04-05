from abjad.container.formatter import _ContainerFormatter
from abjad.grace.slots import _GraceFormatterSlotsInterface


class _GraceFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _GraceFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slots(self):
      return self._slots

#   @property
#   def slot_2(self):
#      result = [ ]
#      type = self._client.type
#      if type == 'after':
#         result.append('{')
#      else:
#         result.append(r'\%s {' % type)
#      return result
