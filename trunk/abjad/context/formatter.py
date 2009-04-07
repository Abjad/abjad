from abjad.container.container import _ContainerFormatter
from abjad.context.slots import _ContextFormatterSlotsInterface


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)
      self._slots = _ContextFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _invocation(self):
      client = self._client
      if client.name is not None:
         return r'\context %s = "%s"' % (client.context, client.name)
      else:
          return r'\new %s' % client.context

   ## PUBLIC ATTRIBUTES ##

   @property
   def context(self):
      return self._client

   @property
   def slots(self):
      return self._slots
