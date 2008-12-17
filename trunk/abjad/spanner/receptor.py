### Use this _SpannerReceptor class as a mix-in from which
### different leaf interfaces can inherit.
### Having a leaf interface inherit from _SpannerReceptor
### indicates that you want the leaf interface to be 'spannable'.
### The 'spanners' variable passed in here at initialization is
### a list of (usually a single) string, like ['Beam'], that says
### to the leaf interface: "please recevie spanners of which the
### classname is 'Beam'.
###
### Note that nowhere in this file is the word 'interface' used,
### except in this comment. 

from abjad.core.abjadcore import _Abjad


class _SpannerReceptor(_Abjad):

   def __init__(self, spanners):
      self._spanners = spanners

   ### PUBLIC ATTRIBUTES ###

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
   def spanned(self):
      return bool(self.spanners)

   @property
   def spanner(self):
      spanners = self.spanners
      if spanners:
         return self.spanners[0]

   @property
   def spanners(self):
      result = [ ]
      for classname in self._spanners:
         result.extend(self._client.spanners.get(classname = classname))
      return result

   ### PUBLIC METHODS ###

   def unspan(self):
      for spanner in self.spanners[ : ]:
         spanner.die( )
