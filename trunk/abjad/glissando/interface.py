from .. core.interface import _Interface
from .. core.parser import _Parser

class GlissandoInterface(_Interface):

   def __init__(self, client):
      self._client = None
      self._parser = _Parser( )
      self._set = None

   def __nonzero__(self):
      return bool(self._set)

   def __eq__(self, arg):
      assert isinstance(arg, bool)
      return bool(self._set) == arg

   def clear(self):
      self._set = None
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            delattr(self, key)

   @property
   def _before(self):
      result = [ ]
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            result.append('\once \override Glissando %s = %s' % (
               self._parser.formatAttribute(key),
               self._parser.formatValue(value)))
      return result

   @property
   def _right(self):
      result = [ ]
      if self._set:
         result.append(r'\glissando')
      return result
