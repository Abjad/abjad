from abjad.core.formatter import _Formatter


class _NoteHeadFormatter(_Formatter):

   def __init__(self, client):
      _Formatter.__init__(self, client)

   @property
   def _lily(self):
      assert self._client.pitch
      result = [ ]
      result.extend(self._client._before)
      result.append(self._client.pitch.lily)
      return result

   @property
   def lily(self):
      return '\n'.join(self._lily)
