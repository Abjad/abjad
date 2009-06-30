from abjad.leaf.leaf import _Leaf
from abjad.pitch import Pitch
from abjad.rest.initializer import _RestInitializer


class Rest(_Leaf):
   '''The `Abjad` model of a single rest.'''

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
      '''Read-only list of string representation of body of rest.
      Picked up as format contribution at format-time.'''
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
   def numbers(self):
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )
  
   @property
   def pairs(self):
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )

   @apply
   def pitch( ):
      def fget(self):
         '''Read / write value for so-called pitched rest.'''
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
      '''Read-only empty tuple because rests have no pitch.'''
      return ( )
