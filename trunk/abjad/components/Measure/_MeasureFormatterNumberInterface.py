from abjad.core import _StrictComparator


class _MeasureFormatterNumberInterface(_StrictComparator):

   def __init__(self, _client):
      self._client = _client
      self._leaves = None
      self._self = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _measure_contribution(self):
      if self.self is not None:
         return self.self
      parentage = self._client._client.parentage.proper_parentage
      for parent in parentage:
         if hasattr(parent._formatter, 'number'):
            contribution = getattr(parent._formatter.number, 'measures', None)
            if contribution is not None:
               return contribution
      return None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def leaves( ):
      def fget(self):
         return self._leaves
      def fset(self, arg):
         assert arg in ('comment', 'markup', None)
         self._leaves = arg
      return property(**locals( ))
         
   @apply
   def self( ):
      def fget(self):
         return self._self
      def fset(self, arg):
         assert arg in ('comment', None)
         self._self = arg
      return property(**locals( ))
