from abjad.container.slots import _ContainerFormatterSlotsInterface


class _GraceFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      type = self._client._client.type
      if type == 'after':
         result.append('{')
      else:
         result.append(r'\%s {' % type)
      return tuple(result)
