from abjad.interfaces.grace.interface import GraceInterface
from abjad.tools.scoretools.donate import donate


## TODO: Change way we determine what attributes to transfer. ##

_attributes_not_to_copy = ('_formatter', '_parentage', '_spanners')
   
def _transfer_all_attributes(old, new):
   donate([old], new)
   for key, value in sorted(vars(old).items( )):
      if key not in _attributes_not_to_copy:
         if hasattr(value, '_client'):
            setattr(value, '_client', new)
            if isinstance(value, GraceInterface):
               setattr(value._after, '_carrier', new)
               setattr(value._before, '_carrier', new)
         setattr(new, key, value)
