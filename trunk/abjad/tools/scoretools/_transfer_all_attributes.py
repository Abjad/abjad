from abjad.tools import componenttools


## TODO: Change way we determine what attributes to transfer. ##

_attributes_not_to_copy = ('_formatter', '_parentage', '_spanners')
   
def _transfer_all_attributes(old, new):
   componenttools.move_parentage_and_spanners_from_components_to_components([old], [new])
   for key, value in sorted(vars(old).items( )):
      if key not in _attributes_not_to_copy:
         if hasattr(value, '_client'):
            setattr(value, '_client', new)
         setattr(new, key, value)
