class _ParentReceipt(object):
   '''Class to encapsulate parent of Abjad component
      and index-in-parent of Abjad component.'''

   def __init__(self, component, parent, index):
      self._component = component
      self._parent = parent
      self._index = index
