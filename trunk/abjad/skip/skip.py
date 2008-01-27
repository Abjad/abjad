from .. leaf.leaf import Leaf
from initializer import SkipInitializer

class Skip(Leaf):

   def __init__(self, *args):
      self.initializer = SkipInitializer(self, Leaf, *args)
      
   ### REPR ###

   def __repr__(self):
      return 'Skip(%s)' % self.duration._product

   def __str__(self):
      return 's%s' % self.duration._product

   ### FORMATTING ###
  
   @property
   def _body(self):
      return 's%s' % self.duration._product
