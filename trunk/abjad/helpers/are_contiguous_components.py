from abjad.helpers.are_threadable_components import _are_threadable_components
from abjad.component.component import _Component


def _are_contiguous_components(expr):
   '''True when expr is a Python list and when
         
         1. every element in list is an Abjad component,
         2. all components are threadable, and
         3. all components are temporally successive.

      Otherwise False.

      BY DEFINITION 'contiguous' means 'threadable and successive'.'''
   
   if isinstance(expr, list):
      if len(expr) == 0:
         return True
      first = expr[0]
      if isinstance(first, _Component):
         first_signature = first.parentage._containmentSignature
         prev = first
         for cur in expr[1:]:
            if not isinstance(cur, _Component):
               return False
            cur_signature = cur.parentage._containmentSignature
            if not cur_signature == first_signature:
               return False
            if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
               return False
            prev = cur
         return True
   return False
