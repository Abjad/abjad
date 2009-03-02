### Use this _SpannerReceptor class as a mix-in from which
### different leaf interfaces can inherit.
### Having a leaf interface inherit from _SpannerReceptor
### indicates that you want the leaf interface to be 'spannable'.
### The 'spanners' variable passed in here at initialization is
### a list of (usually a single) string, like ['Beam'], that says
### to the leaf interface: "please recevie spanners of which the
### classname is 'Beam'".

from abjad.core.abjadcore import _Abjad
from abjad.exceptions.exceptions import ExtraSpannerError
from abjad.exceptions.exceptions import MissingSpannerError
from abjad.helpers.hasname import hasname


class _SpannerReceptor(_Abjad):

   def __init__(self, classnames):
      self._classnames = classnames

   ### PUBLIC ATTRIBUTES ###

   @property
   def count(self):
      return len(self.spanners)

   @property
   def first(self):
      return self.spanned and self.spanner._isMyFirstLeaf(self._client)

   @property
   def last(self):
      return self.spanned and self.spanner._isMyLastLeaf(self._client)

   @property
   def only(self):
      return self.spanned and self.spanner._isMyOnlyLeaf(self._client)

   @property
   def position(self):
      count = self.count
      if count == 0:
         raise MissingSpannerError
      elif count == 1:
         return self.spanner.index(self._client)
      else:
         raise ExtraSpannerError

   @property
   def spanned(self):
      return bool(self.spanners)

   @property
   def spannedAbove(self):
      '''
      Returns true is a spanner of this type is attached to self or
      if it's attached to a parent.
      '''
      result =  [ ]
      parentage = self._client._parentage.parentage
      for parent in parentage:
         spanners = parent.spanners.attached
         for classname in self._classnames:
            result.extend([p for p in spanners if hasname(p, classname)])
      return bool(result)

   @property
   def spanner(self):
      spanners = self.spanners
      if spanners:
         return self.spanners[0]

   @property
   def spanners(self):
      result = [ ]
      client = self._client
      for classname in self._classnames:
         spanners = client.spanners.attached
         result.extend([p for p in spanners if hasname(p, classname)])
      return result

   ### PUBLIC METHODS ###

   def unspan(self):
      result = [ ]
      for spanner in self.spanners[ : ]:
         spanner.clear( )
         result.append(spanner)
      return result
