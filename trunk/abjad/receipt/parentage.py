from abjad.core.abjadcore import _Abjad


class _ParentageReceipt(_Abjad):
   '''Class to encapsulate parent and index-in-parent of Abjad component.
      Encapsulated return type of _Parentage.detach( ).
      Expected input type of _Parentage.reattach( ).'''

   def __init__(self, component, parent, index):
      self._component = component
      self._parent = parent
      self._index = index

   ## PRIVATE METHODS ##

   def _empty(self):
      self._component = None
      self._parent = None
      self._index = None
