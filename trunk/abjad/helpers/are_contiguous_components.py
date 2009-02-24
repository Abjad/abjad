from abjad.component.component import _Component


def _are_contiguous_components(component_list):
   '''
   True when component_list is a Python list and when
   each of the elements in component_list:

      1. is an Abjad component
      2. has the same parent
      3. appears -- in order -- in parent.

   Otherwise False.

   Intended for type-checking helper function input.

   TODO: 

   Replace with newer, threading-based check.
   '''

   try:
      assert isinstance(component_list, list)
      if len(component_list) == 0:
         return True
      else:
         first_component = component_list[0]
         assert isinstance(first_component, _Component)
         assert first_component.parentage.parent is not None
         first_parent = first_component.parentage.parent
         first_index_in_parent = first_parent.index(first_component)
      for i, element in enumerate(component_list):
         assert element is first_parent[first_index_in_parent + i]
      return True
   except (AssertionError, IndexError):
      return False
