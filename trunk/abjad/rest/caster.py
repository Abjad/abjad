from .. core.caster import _Caster

class RestCaster(_Caster):

   def __init__(self, client):
      _Caster.__init__(self, client)

   def toNote(self):
      from .. note.note import Note
      result = Note( )
      self._transferAllAttributesTo(result)
      return result

   def toChord(self):
      from .. chord.chord import Chord
      result = Chord([ ])
      self._transferAllAttributesTo(result)
      return result

   def toSkip(self):
      from .. skip.skip import Skip
      result = Skip( )
      self._transferAllAttributesTo(result)
      return result
