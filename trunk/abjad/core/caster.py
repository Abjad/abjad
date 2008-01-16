class _Caster(object):

   def __init__(self, client):
      self._client = client

   def __repr__(self):
      return '%s( )' % self.__class__.__name__

   ### TODO - decide whether we wanna keep the current way of
   ###        determining which attributes to transfer.
   ###        right now we transfer all attributes except self.caster;
   ###        (which we do to keep final self._client.__dict__.clear( )
   ###        from clearing *leaf* instead of *self*);
   ###        and also self.formatter (because self.formatter is class-
   ###        specific);
   ###        should we transfer all attributes (save caster & formatter)?
   ###        or are there other attrs that we should refuse to transfer?

   def _transferAllAttributesTo(self, leaf):
      if self._client._parent:
         self._client._parent[self._client._parent.index(self._client)] = leaf
      del self._client._parent
      for key, value in self._client.__dict__.items( ):
         if key not in ['caster', 'formatter']:
            leaf.__dict__[key] = value
            if hasattr(value, '_client'):
               value._client = leaf
            if hasattr(value, '_parent'):
               raise ValueError('attr %s should not have _parent.' % value)
      leaf.formatter.before.extend(self._client.formatter.before)
      leaf.formatter.after.extend(self._client.formatter.after)
      leaf.formatter.left.extend(self._client.formatter.left)
      leaf.formatter.right.extend(self._client.formatter.right)
      self._client.__dict__.clear( )

   def _friendlyTransferAllAttributesTo(self, leaf):
      for key, value in self._client.__dict__.items( ):
         leaf.__dict__[key] = value._clone(leaf)
