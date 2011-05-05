from abjad.tools.componenttools._ContainmentSignature import _ContainmentSignature


def component_to_parentage_signature(component):
   '''.. versionadded:: 1.1.1

   Change `component` to parentage signature::

      abjad> tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> staff = Staff([tuplet])
      abjad> note = staff.leaves[0]
      abjad> print componenttools.component_to_parentage_signature(note)
            root: Staff-18830800 (18830800)
           score: 
      staffgroup: 
           staff: Staff-18830800
           voice: 
            self: Note-18619728

   Return parentage signature.
   '''
   from abjad.components import Score
   from abjad.components import Staff
   from abjad.components import Voice
   from abjad.tools import componenttools
   from abjad.tools.scoretools import StaffGroup

   signature = _ContainmentSignature( )
   signature._self = component._ID
   for component in componenttools.get_improper_parentage_of_component(component):
      if isinstance(component, Voice) and not signature._voice:
         signature._voice = component._ID
      elif isinstance(component, Staff) and not signature._staff:
         signature._staff = component._ID
      elif isinstance(component, StaffGroup) and not signature._staffgroup:
         signature._staffgroup = component._ID
      elif isinstance(component, Score) and not signature._score:
         signature._score = component._ID
   else:
      '''Root components must be manifestly equal to compare True.'''
      signature._root = id(component)
      signature._root_str = component._ID
   return signature
