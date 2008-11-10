from abjad.core.interface import _Interface


class _HarmonicInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._set = None

   ### OVERLOADS ###

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def __nonzero__(self):
      return bool(self._set)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\flageolet')
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      self._set = None
      ### NOTE: why is this here?
      _GrobHandler.clear(self)
