from .. leaf.leaf import Leaf
from initializer import RestInitializer

class Rest(Leaf):

   def __init__(self, *args):
      self.initializer = RestInitializer(self, Leaf, *args )
   

   ### REPR ###

   def __repr__(self):
      if self._product:
         return 'Rest(%s)' % self._product
      else:
         return 'Rest( )'

   def __str__(self):
      if self._product:
         return 'r%s' % self._product
      else:
         return ''

   ### FORMATTING ###
  
   @property
   def _body(self):
      if self._product:
         return 'r%s' % self._product
      else:
         return ''
