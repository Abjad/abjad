from abjad.component.component import _Component


def _are_containerized_components(expr):
   '''True when expr is a Python list and when

         1. every element in list is an Abjad component, 
         2. every component in list has a parent,
         2. all components parents are the same.

      Otherwise False.

      Note that components need not be ordered temporally in any way.'''

   if isinstance(expr, list):
      if len(expr) == 0:
         return True
      first = expr[0]
      if isinstance(first, _Component):
         first_parent = first.parentage.parent
         if first_parent is None:
            return False
         for element in expr[1:]:
            if not isinstance(element, _Component):
               return False
            if not element.parentage.parent is first_parent:
               return False
         return True
   return False
