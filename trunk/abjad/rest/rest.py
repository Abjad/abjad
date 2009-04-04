from abjad.leaf.leaf import _Leaf
from abjad.pitch.pitch import Pitch
from abjad.rest.initializer import _RestInitializer


class Rest(_Leaf):

   def __init__(self, *args):
      self._initializer = _RestInitializer(self, _Leaf, *args)
   
   ## OVERLOADS ##

   def __repr__(self):
      return 'Rest(%s)' % self.duration._product

   def __str__(self):
      return 'r%s' % self.duration._product

   ## PUBLIC ATTRIBUTES ##

   @property
   def body(self):
      '''String representation of body of rest at format-time.
         Return list like all other format-time contributions.'''
      result = ''
      if self.pitch:
         result += str(self.pitch)
      else:
         result += 'r'
      result += str(self.duration._product)
      if self.pitch:
         result += r' \rest'
      return [result]
  
   @property
   def pairs(self):
      return ( )

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

   @property
   def pitches(self):
      return ( )
