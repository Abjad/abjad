from abjad.core.abjadcore import _Abjad
from abjad.exceptions import ExtraSpannerError
from abjad.exceptions import MissingSpannerError


class _SpannerReceptor(_Abjad):
   '''Abstract base class to mix in with component interfaces.
      _SpannerReceptor confers the ability to receive spanners.'''

   def __init__(self, klasses):
      '''`klasses` should be a tuple of one or more spanner classes.'''
      self._klasses = klasses

   ## PUBLIC ATTRIBUTES ##

   @property
   def chain(self):
      '''Return tuple of all leaves in spanner, if spanned;
         otherwise return 1-tuple of client.'''
      count = self.count
      if count == 0:
         return (self._client, )
      elif count == 1:
         return tuple(self.spanner.leaves)
      else:
         raise ExtraSpannerError

   @property
   def count(self):
      '''Return number of spanners attaching to client.'''
      return len(self.spanners)

   @property
   def first(self):
      '''True when client is first in spanner, otherwise False.'''
      return self.spanned and self.spanner._isMyFirstLeaf(self._client)

   @property
   def last(self):
      '''True when client is last in spanner, otherwise False.'''
      return self.spanned and self.spanner._isMyLastLeaf(self._client)

   @property
   def only(self):
      '''True when client is only leaf in spanner, otherwise False.'''
      return self.spanned and self.spanner._isMyOnlyLeaf(self._client)

   @property
   def parented(self):
      '''True when spanner attached to any component in parentage of client,
         including client, otherwise False.'''
      result =  [ ]
      parentage = self._client.parentage.parentage
      for parent in parentage:
         spanners = parent.spanners.attached
         for klass in self._klasses:
            result.extend(
               [p for p in spanners if isinstance(p, klass)])
      return bool(result)

   @property
   def position(self):
      '''Return zero-indexed position of client in spanner.'''
      count = self.count
      if count == 0:
         raise MissingSpannerError
      elif count == 1:
         return self.spanner.index(self._client)
      else:
         raise ExtraSpannerError

   @property
   def spanned(self):
      '''True when client is spanned.'''
      return bool(self.spanners)

   @property
   def spanner(self):
      '''Return first spanner attaching to client.'''
      count = self.count
      if count == 0:
         raise MissingSpannerError
      elif count == 1:
         return list(self.spanners)[0]
      else:
         raise ExtraSpannerError

   @property
   def spanner_in_parentage(self):
      '''Return first spanner attaching to parentage of client.'''
      parentage = self._client.parentage.parentage
      for parent in parentage:
         spanners = parent.spanners.attached
         for klass in self._klasses:
            for spanner in spanners:
               if isinstance(spanner, klass):
                  return spanner
      raise MissingSpannerError
      
   @property
   def spanners(self):
      '''Return all spanners attaching to client.'''
      result = set([ ])
      client = self._client
      for klass in self._klasses:
         spanners = client.spanners.attached
         result.update([p for p in spanners if isinstance(p, klass)])
      return result

   ## PUBLIC METHODS ##

   def unspan(self):
      '''Remove all spanners attaching to client.'''
      result = [ ]
      for spanner in list(self.spanners):
         spanner.clear( )
         result.append(spanner)
      return result
