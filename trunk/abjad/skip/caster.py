from .. core.caster import _Caster

class SkipCaster(_Caster):

   def __init__(self, client):
      _Caster.__init__(self, client)

   def toNote(self):
      from .. note.note import Note
      result = Note( )
      self._transferAllAttributesTo(result)
      return result

   def toRest(self):
      from .. rest.rest import Rest
      result = Rest( )
      self._transferAllAttributesTo(result)
      return result

   def toChord(self):
      from .. chord.chord import Chord
      result = Chord([ ])
      self._transferAllAttributesTo(result)
      return result
