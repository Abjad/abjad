class _SpannerReceptor(object):

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

   ### PUBLIC METHODS ###

   def unspan(self):
      for spanner in self.spanners[ : ]:
         spanner.die( )
