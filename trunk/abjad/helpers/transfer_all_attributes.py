### TODO - decide whether we wanna keep the current way of
###        determining which attributes to transfer.
###        right now we transfer all attributes except self.caster;
###        (which we do to keep final self._client.__dict__.clear( )
###        from clearing *leaf* instead of *self*);
###        and also self.formatter (because self.formatter is class-
###        specific);
###        should we transfer all attributes (save caster & formatter)?
###        or are there other attrs that we should refuse to transfer?

_attributes_not_to_copy = (
   '_formatter', 
   '_grob', 
   '_parser', 
   '_promotions', 
   '_spanners',
   )
   
def _transfer_all_attributes(old, new):
   oldCopy = old.copy( )
   for key, value in oldCopy.__dict__.items( ):
      if key not in _attributes_not_to_copy:
         if hasattr(value, '_client'):
            setattr(value, '_client', new)
         setattr(new, key, value)
   new._parent = old._parent
   old._parent = None
   if new._parent:
      new._parent._music[new._parent.index(old)] = new
   #for spanner in old.spanners:
   #for spanner in old.spanners.mine( ):
   for spanner in old.spanners.spanners:
      #spanner._receptors[spanner.index(old)] = new.spanners
      #spanner._leaves[spanner.index(old)] = new
      spanner._components[spanner.index(old)] = new
      new.spanners._append(spanner)
   new.formatter.before.extend(oldCopy.formatter.before)
   new.formatter.after.extend(oldCopy.formatter.after)
   new.formatter.left.extend(oldCopy.formatter.left)
   new.formatter.right.extend(oldCopy.formatter.right)
   old.spanners = oldCopy.spanners
   old.spanners._client = old
   del oldCopy
