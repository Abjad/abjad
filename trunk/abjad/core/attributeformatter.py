from abjad.core.parser import _Parser


class _AttributeFormatter(object):

   def __init__(self, grob):
      self._grob = grob
      self._parser = _Parser( )

   ### OVERLOADS ###

   def __len__(self):
      return len([kvp for kvp in self.__dict__.items( ) 
         if not kvp[0].startswith('_')])

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in self.__dict__:
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ### PRIVATE ATTRIBUTES ###

   @property
   def _before(self):
      result = [ ]
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            result.append(r'\once \override %s %s = %s' % (
               self._grob, 
               self._parser.formatAttribute(key),
               self._parser.formatValue(value)))
      return result

   ### PUBLIC METHODS ###

   def clear(self):
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            delattr(self, key)
