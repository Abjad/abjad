from abjad.component.component import _Component


def _are_orphan_components(component_list):
   '''
   True when component_list is a Python list and when
   each of the elements in component_list

      1. is an Abjad component, and
      2. has no parent.

   Otherwise False.

   Intended to type-check helper function input.
   '''

   try:
      assert isinstance(component_list, list)
      for element in component_list:
         assert isinstance(element, _Component)
         assert element.parentage.orphan
      return True
   except AssertionError:
      return False
