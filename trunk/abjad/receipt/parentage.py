class ParentageReceipt(object):
   '''Class to encapsulate parent and index-in-parent 
      of any Abjad component.'''

   def __init__(self, component, parent, index):
      self.component = component
      self.parent = parent
      self.index = index
