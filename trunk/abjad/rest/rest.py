from .. leaf.leaf import Leaf
from initializer import RestInitializer
from .. pitch.pitch import Pitch

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

   ### PROPERTIES ###
   @apply
   def pitch( ):
      def fget(self):
          return self._pitch
      def fset(self, arg):
         if isinstance(arg, type(None)):
            self._pitch = None
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         elif isinstance(arg, tuple):
            self._pitch = Pitch(*arg)
         elif isinstance(arg, Pitch):
            self._pitch = arg
         else:
            raise ValueError('Can not set Rest.pitch from %s' % str(arg))
      return property(**locals( ))

   ### FORMATTING ###
  
   @property
   def _body(self):
#      if self._product:
#         if self.pitch:
#            return '%s%s\\rest' % (self.pitch, self._product)
#         else:
#            return 'r%s' % self._product
#      else:
#         return ''

      result = ''
      if self.pitch:
         result += str(self.pitch)
      else:
         result += 'r'
      if self._product:
         result += str(self._product)
      if self.pitch:
         result += r' \rest'
      if self.stem.tremolo:
         result += ' :%s' % self.stem.tremolo
      return result
