from abjad.tools import clone
from abjad.tools import scoretools


## TODO - decide whether we wanna keep the current way of
##        determining which attributes to transfer.
##        right now we transfer all attributes except self.caster;
##        (which we do to keep final self._client.__dict__.clear( )
##        from clearing *leaf* instead of *self*);
##        and also self.formatter (because self.formatter is class-
##        specific);
##        should we transfer all attributes (save caster & formatter)?
##        or are there other attrs that we should refuse to transfer?

_attributes_not_to_copy = (
   '_formatter', 
   '_grob', 
   '_parser', 
   '_promotions', 
   '_spanners',
   )
   
def _transfer_all_attributes(old, new):
   from abjad.grace.interface import _GraceInterface
   oldCopy = clone.fracture([old])[0]
   for key, value in oldCopy.__dict__.items( ):
      if key not in _attributes_not_to_copy:
         if hasattr(value, '_client'):
            setattr(value, '_client', new)
            ## take care of Grace._parent
            if isinstance(value, _GraceInterface):
               setattr(value.after, '_carrier', new)
               setattr(value.before, '_carrier', new)
         setattr(new, key, value)
   scoretools.donate([old], new)
   try:
      new.formatter.before.extend(oldCopy.formatter.before)
      new.formatter.after.extend(oldCopy.formatter.after)
   except AttributeError:
      pass
   try:
      new.formatter.left.extend(oldCopy.formatter.left)
      new.formatter.right.extend(oldCopy.formatter.right)
   except AttributeError:
      pass
   old._spanners = oldCopy.spanners
   old.spanners._client = old
   del oldCopy
