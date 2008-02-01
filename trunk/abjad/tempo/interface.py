from .. core.interface import _Interface

class _TempoInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'MetronomeMark', ['Tempo'])
      self._metronome = None
 
   ### OVERRIDES ###

   def __nonzero__(self):
      return bool(self._metronome)

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._metronome) == arg


   ### METHODS ###

   def clear(self):
      self._metronome = None
      _Interface.clear(self)

   ### FORMATTING ###
   
   @property
   def _before(self):
      result =  [ ] 
      if self._metronome:
         note = self._metronome[0].duration._dotted 
         tempo = self._metronome[1]
         result.append(r'\tempo %s=%s' % (note, tempo))
      return result


