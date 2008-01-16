from .. core.caster import _Caster

class NoteCaster(_Caster):

   def __init__(self, client):
      self._client = client

   def toRest(self):
      from .. rest.rest import Rest
      result = Rest( )
      self._transferAllAttributesTo(result)
      #self._transferAllAttributesTo_old(result)
      return result

   def toChord(self):
      from .. chord.chord import Chord
      result = Chord([ ])
      if self._client.notehead:
         result.append(self._client.notehead)
      self._transferAllAttributesTo(result)
      return result

   def toSkip(self):
      from .. skip.skip import Skip
      result = Skip( )
      self._transferAllAttributesTo(result)
      return result
