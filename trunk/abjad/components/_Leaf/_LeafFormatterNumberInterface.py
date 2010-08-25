class _LeafFormatterNumberInterface(object):

   __slots__ = ('_client', 'self', )

   def __init__(self, client):
      self._client = client
      ## set to 'comment' or 'markup'
      self.self = None

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
