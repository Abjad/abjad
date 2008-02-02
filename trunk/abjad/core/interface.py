from .. core.parser import _Parser

class _Interface(object):

   def __init__(self, client, grob, spanners):
      self._client = client
      self._grob = grob
      self._parser = _Parser( )
      self._spanners = spanners

   ### REPR ###

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   ### OVERRIDES ###

   def __len__(self):
      return len([kvp for kvp in self.__dict__.items( ) 
         if not kvp[0].startswith('_')])

   def __setattr__(self, attr, value):
      if not attr.startswith('_') and value is None and attr in self.__dict__:
         delattr(self, attr) 
      else:
         object.__setattr__(self, attr, value)

   ### PROPERTIES ###

   @property
   def spanners(self):
      result = [ ]
      for classname in self._spanners:
         result.extend(self._client.spanners.get(classname = classname))
      return result

   @property
   def spanner(self):
      spanners = self.spanners
      if spanners:
         return self.spanners[0]

   @property
   def spanned(self):
      return bool(self.spanners)

   @property
   def first(self):
      return self.spanned and self.spanner._isMyFirstLeaf(self._client)

   @property
   def last(self):
      return self.spanned and self.spanner._isMyLastLeaf(self._client)

   @property
   def only(self):
      return self.spanned and self.spanner._isMyOnlyLeaf(self._client)

   ### METHODS ###

   def clear(self):
      for key, value in self.__dict__.items( ):
         if not key.startswith('_'):
            delattr(self, key)

   def unspan(self):
      for spanner in self.spanners[ : ]:
         spanner.die( )

   def copy(self):
      from copy import copy
      client = self._client
      self._client = None
      result = copy(self)
      self._client = client
      return result

   ### FORMATTING ###

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
