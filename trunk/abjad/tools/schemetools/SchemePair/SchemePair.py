from abjad.core import _Immutable
from types import BooleanType


class SchemePair(tuple, _Immutable):
   '''Abjad representation of Scheme pair.'''

   def __new__(klass, *args):
      if len(args) != 2:
         raise Exception('Scheme pairs may contain only two values.')
      self = tuple.__new__(klass, args)
      return self

   def __getnewargs__(self):
      return tuple(self)

#   def __init__(self, *args):
#      if 2 < len(args):
#          raise Exception('Scheme pairs may contain only two values.')
#      list.__init__(self, args)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   def __str__(self):
      return '(%s)' % self._output_string
   
   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([str(x) for x in self])

   @property
   def _output_string(self):
      vals = []
      for x in self:
          if isinstance(x, BooleanType) and x:
              vals.append("#t")
          elif isinstance(x, BooleanType):
              vals.append("#f")
          else:
              vals.append(x)
      return '%s . %s' % (vals[0], vals[1])

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''LilyPond input representation of scheme pair.'''
      return "#'%s" % self.__str__()
