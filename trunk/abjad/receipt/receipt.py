from abjad.core.abjadcore import _Abjad
from abjad.receipt.parentage import ParentageReceipt
from abjad.receipt.spanners import SpannersReceipt


class Receipt(_Abjad):
   '''Well structured references attaching to some Abjad component.'''

   def __init__(self, parentage, spanners):
      self._parentage = parentage
      self._spanners = spanners

   ## PRIVATE METHODS ##

   def _empty(self):
      self._parentage = None
      self._spanners = None
