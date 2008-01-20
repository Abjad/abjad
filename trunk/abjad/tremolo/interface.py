from .. core.interface import _Interface

class TremoloInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Tremolo', ['Tremolo'])
      self._subdivision = None

   ### ACCESSORS ###

   def __repr__(self):
      if self.subdivision:
         return 'Tremolo(%s)' % self.subdivision
      else:
         return 'Tremolo( )'

   ### MANAGED ###

   @apply
   def subdivision( ):
      def fget(self):
         return self._subdivision
      def fset(self, expr):
         self._subdivision = expr
      return property(**locals())

   ### FORMATTING ###

   @property
   def body(self):
      if self.subdivision:
         return ':' + str(self.subdivision)
      else:
         return ''
