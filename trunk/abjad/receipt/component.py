from abjad.core.abjadcore import _Abjad
from abjad.receipt.parentage import _ParentageReceipt
from abjad.receipt.spanner import _SpannerReceipt


class _ComponentReceipt(_Abjad):
   '''Well structured references attaching to some Abjad component.'''

   def __init__(self, component, parentage, spanners):
      self._component = component
      self._parentage = parentage
      self._spanners = spanners

   ## PRIVATE METHODS ##

   def _empty(self):
      self._component = None
      self._parentage = None
      self._spanners = None
