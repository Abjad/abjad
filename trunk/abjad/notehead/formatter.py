from abjad.core.formatter import _Formatter


class _NoteHeadFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   ### PRIVATE ATTRIBUTES ###

   @property
   #def _lily(self):
   def _format(self):
      assert self._client.pitch
      result = [ ]
      result.extend(self._client._before)
      #result.append(self._client.pitch.lily)
      result.append(self._client.pitch.format)
      return result

   ### PUBLIC ATTRIBUTES ###

   @property
   #def lily(self):
   #   return '\n'.join(self._lily)
   def format(self):
      return '\n'.join(self._format)
