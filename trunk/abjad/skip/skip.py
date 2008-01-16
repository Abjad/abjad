from caster import SkipCaster
from .. leaf.leaf import Leaf

class Skip(Leaf):

   def __init__(self, duration = None):
      Leaf.__init__(self)
      self.caster = SkipCaster(self)
      self.duration = duration
      
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
