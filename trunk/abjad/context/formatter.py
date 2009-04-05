from abjad.container.container import _ContainerFormatter
from abjad.context.slots import _ContextFormatterSlotsInterface


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _ContextFormatterSlotsInterface(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def INVOCATION(self):
      client = self._client
      if client.name is not None:
         return r'\context %s = "%s"' % (client.context, client.name)
      else:
          return r'\new %s' % client.context

   @property
   def slots(self):
      return self._slots
