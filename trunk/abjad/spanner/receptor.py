## Use this _SpannerReceptor class as a mix-in from which
## different leaf interfaces can inherit.
## Having a leaf interface inherit from _SpannerReceptor
## indicates that you want the leaf interface to be 'spannable'.
## The 'spanners' variable passed in here at initialization is
## a list of (usually a single) string, like ['Beam'], that says
## to the leaf interface: "please recevie spanners of which the
## classname is 'Beam'".

from abjad.core.abjadcore import _Abjad
from abjad.exceptions.exceptions import ExtraSpannerError
from abjad.exceptions.exceptions import MissingSpannerError


class _SpannerReceptor(_Abjad):

   def __init__(self, classreferences):
      self._classreferences = classreferences

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
         for classreference in self._classreferences:
            result.extend(
               [p for p in spanners if isinstance(p, classreference)])
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
         return self.spanners[0]
      else:
         raise ExtraSpannerError

   @property
   def spanners(self):
      '''Return all spanners attaching to client.
         TODO: return unordered set.'''
      result = [ ]
      client = self._client
      for classreference in self._classreferences:
         spanners = client.spanners.attached
         result.extend([p for p in spanners if isinstance(p, classreference)])
      return result

   ## PUBLIC METHODS ##

   def unspan(self):
      '''Remove all spanners attaching to client.'''
      result = [ ]
      for spanner in self.spanners[ : ]:
         spanner.clear( )
         result.append(spanner)
      return result
