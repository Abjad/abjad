class _ParentageReceipt(object):
   '''Class to encapsulate parent and index-in-parent 
      of any Abjad component.'''

   def __init__(self, component, parent, index):
      self._component = component
      self._parent = parent
      self._index = index
