from .. leaf.leaf import Leaf
from initializer import SkipInitializer

class Skip(Leaf):

   def __init__(self, *args):
      self.initializer = SkipInitializer(self, Leaf, *args)
      
   ### REPR ###

   def __repr__(self):
      if self._product:
         return 'Skip(%s)' % self._product
      else:
         return 'Skip( )'

   def __str__(self):
      if self._product:
         return 's%s' % self._product
      else:
         return ''

   ### FORMATTING ###
  
   @property
   def _body(self):
      if self._product:
         return 's%s' % self._product
      else:
         return 'Skip( )'
