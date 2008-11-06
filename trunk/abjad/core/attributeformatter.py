from abjad.core.parser import _Parser

### INTRO ###
### created from _Interface on 2008-11-04;
### _Interface was doing two different things
### that needed to be broken apart:
###   1. allowing for arbitrary LilyPond attribute formatting
###   2. some stuff with spanners
### this new _AttributeFormatter class implements
### the arbitrary LilyPond attribute formatting stuff only.

class _AttributeFormatter(object):

   #def __init__(self, client, grob, spanners):
   def __init__(self, grob):
      #self._client = client
      self._grob = grob
      self._parser = _Parser( )
      #self._spanners = spanners

#   ### OVERRIDES ###
#
#   def __cmp__(self, arg):
#      raise Exception(NotImplemented)
#
   def __len__(self):
      return len([kvp for kvp in self.__dict__.items( ) 
         if not kvp[0].startswith('_')])

#   def __repr__(self):
#      return '%s( )' % self.__class__.__name__

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in self.__dict__:
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ### PUBLIC METHODS ###

   def clear(self):
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            delattr(self, key)

   ### PRIVATE ATTRIBUTES & METHODS ###

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

#   def _copy(self):
#      from copy import copy
#      client = self._client
#      self._client = None
#      result = copy(self)
#      self._client = client
#      return result
