from caster import RestCaster
from .. leaf.leaf import Leaf

class Rest(Leaf):

   def __init__(self, duration = None):
      Leaf.__init__(self)
      self.caster = RestCaster(self)
      self.duration = duration
   

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
