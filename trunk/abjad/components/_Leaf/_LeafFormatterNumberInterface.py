class _LeafFormatterNumberInterface(object):

   def __init__(self, client):
      self._client = client
      self._self = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _leaf_contribution(self):
      if self.self is not None:
         return self.self
      parentage = self._client._client.parentage.proper_parentage
      for parent in parentage:
         if hasattr(parent._formatter, 'number'):
            contribution = getattr(parent._formatter.number, 'leaves', None)
            if contribution is not None:
               return contribution
      return None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def self( ):
      def fget(self):
         return self._self
      def fset(self, arg):
         assert arg in ('comment', 'markup', None)
         self._self = arg
