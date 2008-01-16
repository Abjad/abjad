from .. core.caster import _Caster

class ChordCaster(_Caster):

   def __init__(self, client):
      _Caster.__init__(self, client)

   def toNote(self):
      from .. note.note import Note
      result = Note( )
      if len(self._client) > 0:
         result.notehead = self._client.noteheads[0]
      self._transferAllAttributesTo(result)
      return result

   def toRest(self):
      from .. rest.rest import Rest
      result = Rest( )
      self._transferAllAttributesTo(result)
      return result

   def toSkip(self):
      from .. skip.skip import Skip
      result = Skip( )
      self._transferAllAttributesTo(result)
      return result
