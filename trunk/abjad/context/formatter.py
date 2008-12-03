from abjad.containers.container import _ContainerFormatter


class _ContextFormatter(_ContainerFormatter):

   def __init__(self, client):
      _ContainerFormatter.__init__(self, client)

   @property
   def _invocation_opening(self):
      return self._client.invocation._opening

   @property
   def _invocation_closing(self):
      return self._client.invocation._closing
