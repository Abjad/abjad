from .. core.interface import _Interface

class _HarmonicInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Harmonic', ['Harmonic'] )
      self._set = None

   ### OVERRIDES ###

   def __nonzero__(self):
      return bool(self._set)

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   ### METHODS ###

   def clear(self):
      self._set = None
      _Interface.clear(self)

   ### FORMATTING ###

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\flageolet')
      return result
